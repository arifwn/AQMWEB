''' REST API handler '''

from django.utils import simplejson as json
from django.core.cache import cache

from piston.handler import BaseHandler
from piston.utils import rc, throttle

import aqm_utils.server
from aqm_utils.xmlrpc import Client
from aqm_web.models import Server

import wrf.commands
from wrf.models import Task, TaskQueue, ChemData


class ServerStatusHandler(BaseHandler):
    ''' Get status of modelling servers '''
    methods_allowed = ('GET',)

    def read(self, request, server_id):
        try:
            status = aqm_utils.server.get_status(server_id)
        except aqm_utils.server.ServerDoesNotExist:
            return rc.NOT_FOUND
        except IOError:
            return rc.THROTTLED
        except:
            return rc.INTERNAL_ERROR
        
        return status


class ServerHandler(BaseHandler):
    model = Server
    methods_allowed = ('GET',)
    fields = ('id', 'name', 'address', 'port', 'is_enabled',
              'get_rest_url', 'get_status_rest_url')
    
    def read(self, request, server_id=None):
        if server_id is not None:
            try:
                return Server.objects.get(pk=server_id)
            except Server.DoesNotExist:
                return rc.NOT_FOUND
            except ValueError:
                return rc.BAD_REQUEST
        else:
            return Server.objects.filter(is_enabled=True).all()


class ChemDataHandler(BaseHandler):
    model = ChemData
    methods_allowed = ('GET',)
    fields = ('id', 'name', 'description', 'created', 'modified',
              'data', 'worksheets', 'is_removed',
              ('user', ('id', 'username', 'first_name', 'last_name', 'email',
                        'get_full_name')),
              ('parameters', ('worksheet', 'x', 'y', 'lat', 'lon', 'value',
                              'conversion_factor', 'pollutant', 'id', 'created',
                              'modified')))
    
    def read(self, request, chemdata_id=None):
        if chemdata_id is not None:
            try:
                return ChemData.objects.get(pk=chemdata_id, is_removed=False)
            except ChemData.DoesNotExist:
                return rc.NOT_FOUND
            except ValueError:
                return rc.BAD_REQUEST
        else:
            return ChemData.objects.filter(is_removed=False).all()
        

class TaskHandler(BaseHandler):
    model = Task
    methods_allowed = ('GET',)
    fields = ('id', 'name', 'description', 'created', 'modified', 'setting',
              'get_status', 'get_stage', 'get_progress_percent', 'get_rest_url',
              'get_url',
              ('user', ('id', 'username', 'first_name', 'last_name', 'email', 'get_full_name')),
              ('setting', ('max_dom', 'start_date', 'end_date',
                           'dx', 'dy', 'lat', 'lon', 'preview_map')))
    
    def read(self, request, task_id=None, all_user=False):
        
        if task_id is not None:
            try:
                return Task.objects.get(pk=task_id)
            except Task.DoesNotExist:
                return rc.NOT_FOUND
            except ValueError:
                return rc.BAD_REQUEST
        else:
            if all_user:
                # return task created by ALL user
                return Task.objects.extra(order_by=['-created']).all()
            else:
                # only return task created by CURRENT user
                return Task.objects.filter(user=request.user).extra(order_by=['-created']).all()

class TaskControlHandler(BaseHandler):
    methods_allowed = ('POST',)
    
    def create(self, request):
        try:
            command = request.data['command']
            task_id = int(request.data['task_id'])
        except KeyError:
            return rc.BAD_REQUEST
        
        if command == 'run':
            return wrf.commands.run_task(task_id)
        elif command == 'retry':
            return wrf.commands.retry_task(task_id)
        if command == 'rerun':
            return wrf.commands.rerun_task(task_id)
        if command == 'stop':
            return wrf.commands.stop_task(task_id)
        if command == 'cancel':
            return wrf.commands.cancel_task(task_id)
        else:
            return rc.BAD_REQUEST
        
class M2MCommandHandler(BaseHandler):
    ''' Handle communication from RPC Server '''
    methods_allowed = ('POST',)
    
    def create(self, request):
        try:
            command = request.data['command']
            server_id = int(request.data['server_id'])
        except KeyError:
            return rc.BAD_REQUEST
        
        if command == 'retrieve_job':
            # request new modelling job
            data = {}
            data['WRFnamelist'] = ""
            data['WPSnamelist'] = ""
            data['ARWpostnamelist'] = ""
            data['grads_template'] = ""
            
            # if no modelling job, return 404
            # return rc.NOT_FOUND
            