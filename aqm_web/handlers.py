''' REST API handler '''

from django.utils import simplejson as json
from django.core.cache import cache

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from aqm_utils.xmlrpc import Client
from aqm_web.models import Server

import wrf.commands
from wrf.models import Task, TaskQueue


class ServerStatusHandler(BaseHandler):
    ''' Get status of modelling servers '''
    methods_allowed = ('GET',)

    def read(self, request, server_id):
        server_addr_key = 'server_addr_%s' % server_id
        server_addr = cache.get(server_addr_key, None)
        if server_addr is None:
            # TODO: read server info from db
            try:
                srv = Server.objects.get(pk=server_id)
            except Server.DoesNotExist:
                return rc.NOT_FOUND
                
            server_addr = 'https://%s:%d' % (srv.address, srv.port)
            cache.set(server_addr_key, server_addr, 30)
        
        server_utilization_key = 'server_utilization_%s' % server_id
        server_utilization = cache.get(server_utilization_key, None)
        if server_utilization is None:
            c = Client(server_addr)
            try:
                server_utilization = c.server.utilization()
                server_utilization['id'] = server_id
            except:
                # remote server not available at the moment
                return rc.INTERNAL_ERROR
            
            cache.set(server_utilization_key, server_utilization, 5)
        
        return server_utilization


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
        

class TaskHandler(BaseHandler):
    model = Task
    methods_allowed = ('GET',)
    fields = ('id', 'name', 'description', 'created', 'modified', 'setting',
              'get_status', 'get_stage', 'get_progress_percent', 'get_rest_url',
              ('user', ('id', 'username', 'first_name', 'last_name', 'email', 'get_full_name')),
              ('setting', ('get_max_dom', 'get_start_date', 'get_end_date')))
    
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
        
    