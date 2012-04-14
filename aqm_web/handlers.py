''' REST API handler '''

import json

from django.core.cache import cache
from django.contrib import messages

from piston.handler import BaseHandler
from piston.utils import rc, throttle

import aqm_utils.server
from aqm_utils.xmlrpc import Client
from aqm_web.models import Server

import wrf.commands
from wrf.models import Task, TaskQueue, ChemData, PollutantParam


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
    methods_allowed = ('GET', 'POST')
    fields = ('id', 'name', 'description', 'created', 'modified',
              'data', 'worksheets', 'is_removed', 'edit_url',
              ('user', ('id', 'username', 'first_name', 'last_name', 'email',
                        'get_full_name')),
              ('parameters', ('worksheet', 'x', 'y', 'lat', 'lon', 'value',
                              'conversion_factor', 'pollutant', 'id', 'created',
                              'modified', 'row_start', 'row_end', 'data_w', 'data_h')))
    
    def read(self, request, chemdata_id=None, all_user=False):
        if chemdata_id is not None:
            try:
                return ChemData.objects.get(pk=chemdata_id, is_removed=False)
            except ChemData.DoesNotExist:
                return rc.NOT_FOUND
            except ValueError:
                return rc.BAD_REQUEST
        else:
            if all_user:
                return ChemData.objects.filter(is_removed=False).extra(order_by=['-created']).all()
            else:
                return ChemData.objects.filter(is_removed=False, user=request.user).extra(order_by=['-created']).all()
    
    def create(self, request, chemdata_id=None):
        try:
            chemdata_id = request.data['chemdata_id']
            parameters_json = request.data['parameters_json']
            display_message = request.data.get('display_message', 'false')
        except KeyError:
            return rc.BAD_REQUEST
        try:
            chemdata = ChemData.objects.get(pk=chemdata_id, is_removed=False)
        except ChemData.DoesNotExist:
                return rc.NOT_FOUND
        except ValueError:
            return rc.BAD_REQUEST
        
        try:
            parameters = json.loads(parameters_json)
            display_message = json.loads(display_message)
        except ValueError:
            return rc.BAD_REQUEST
        
        # TODO: save the parameters        
        chemdata.parameters.clear()
        for parameter in parameters:
            param_id = parameter.get('id')
            if param_id is None:
                # create a new pollutant parameter
                param_obj = PollutantParam(pollutant=parameter['pollutant'],
                                           worksheet=parameter['worksheet'],
                                           conversion_factor=parameter['conversion_factor'],
                                           row_start=parameter['row_start'],
                                           row_end=parameter['row_end'],
                                           data_w=parameter['data_w'],
                                           data_h=parameter['data_h'],
                                           value=parameter['value'],
                                           lat=parameter['lat'],
                                           lon=parameter['lon'],
                                           x=parameter['x'],
                                           y=parameter['y'])
                param_obj.save()
            
            else:
                try:
                    param_obj = PollutantParam.objects.get(id=param_id)
                except PollutantParam.DoesNotExist:
                    return rc.BAD_REQUEST
                
                param_obj.pollutant=parameter['pollutant']
                param_obj.worksheet=parameter['worksheet']
                param_obj.conversion_factor=parameter['conversion_factor']
                param_obj.row_start=parameter['row_start']
                param_obj.row_end=parameter['row_end']
                param_obj.data_w=parameter['data_w']
                param_obj.data_h=parameter['data_h']
                param_obj.value=parameter['value']
                param_obj.lat=parameter['lat']
                param_obj.lon=parameter['lon']
                param_obj.x=parameter['x']
                param_obj.y=parameter['y']
                param_obj.save()
            
            chemdata.parameters.add(param_obj)            
        
        if display_message:
            messages.success(request, 'Emission data successfully saved!')
        
        return True
    

class TaskHandler(BaseHandler):
    model = Task
    methods_allowed = ('GET')
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
            