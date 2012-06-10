''' REST API handler '''

import json
import urllib
import os

from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse

from piston.handler import BaseHandler
from piston.utils import rc, throttle

import wrf.commands
from wrf.models import Task, TaskQueue, ChemData, PollutantParam


class ChemDataHandler(BaseHandler):
    ''' Get and update ChemData. '''
    model = ChemData
    methods_allowed = ('GET', 'POST')
    fields = ('id', 'name', 'description', 'created', 'modified',
              'data', 'timezone', 'worksheets', 'is_removed', 'edit_url',
              ('user', ('id', 'username', 'first_name', 'last_name', 'email',
                        'get_full_name')),
              ('parameters', ('worksheet', 'x', 'y', 'lat', 'lon', 'value',
                              'conversion_factor', 'pollutant', 'id', 'created',
                              'modified', 'row_start', 'row_end', 'data_w', 'data_h',
                              'hourly_fluctuation', 'get_hourly_fluctuation')))
    
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
                                           y=parameter['y'],
                                           hourly_fluctuation=parameter['hourly_fluctuation'])
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
                param_obj.hourly_fluctuation=parameter['hourly_fluctuation']
                param_obj.save()
            
            chemdata.parameters.add(param_obj)            
        
        if display_message:
            messages.success(request, 'Emission data successfully saved!')
        
        return True
    
    def update(self, request, chemdata_id=None, all_user=False):
        return rc.FORBIDDEN
    
    def delete(self, request, chemdata_id=None, all_user=False):
        return rc.FORBIDDEN
    

class TaskHandler(BaseHandler):
    ''' Get Task list and details. '''
    model = Task
    methods_allowed = ('GET')
    fields = ('id', 'name', 'description', 'created', 'modified', 'setting',
              'get_status', 'get_stage', 'get_progress_percent', 'get_rest_url',
              'get_url', 'error_message', 'kind',
              ('user', ('id', 'username', 'first_name', 'last_name', 'email', 'get_full_name')),
              ('setting', ('max_dom', 'start_date', 'end_date', 'dx', 'dy',
                           'lat', 'lon', 'preview_map', 'domain_map')))
    
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
    
    def create(self, request, task_id=None, all_user=False):
        return rc.FORBIDDEN
    
    def update(self, request, task_id=None, all_user=False):
        return rc.FORBIDDEN
    
    def delete(self, request, task_id=None, all_user=False):
        return rc.FORBIDDEN
    
    
class TaskControlHandler(BaseHandler):
    methods_allowed = ('POST',)
    
    def create(self, request): 
        ''' Perform various operation on a task '''
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
        
    def read(self, request):
        return rc.FORBIDDEN
    
    def update(self, request):
        return rc.FORBIDDEN
    
    def delete(self, request):
        return rc.FORBIDDEN
    

class TaskLogHandler(BaseHandler):
    methods_allowed = ('GET',)
    
    def read(self, request, task_id=None):
        pass
    
    def create(self, request, *args, **kwargs):
        return rc.FORBIDDEN
    
    def update(self, request, *args, **kwargs):
        return rc.FORBIDDEN
    
    def delete(self, request, *args, **kwargs):
        return rc.FORBIDDEN
    
    
class M2MCommandHandler(BaseHandler):
    ''' Handle communication from RPC Server '''
    methods_allowed = ('POST',)
    
    def read(self, request):
        return rc.FORBIDDEN
    
    def update(self, request):
        return rc.FORBIDDEN
    
    def delete(self, request):
        return rc.FORBIDDEN
    
    def create(self, request):
        try:
            command = request.data['command']
            server_id = int(request.data['server_id'])
        except KeyError:
            return rc.BAD_REQUEST
        
        data = request.data.get('data')
        if data is not None:
            try:
                data = json.loads(data)
            except ValueError:
                data = {}
        
        if command == 'retrieve_job':
            # request new modelling job
            # if no modelling job, return 404
            # return rc.NOT_FOUND
            return self.retrieve_job(server_id)
        
        elif command == 'confirm_run':
            # the server is about to run specified job.
            # if the handle return True, it will continue
            # if false, it will cancel the job
            task_id = data.get('task_id')
            if task_id is None:
                return rc.BAD_REQUEST
            
            return self.confirm_run(server_id, task_id)
        
        elif command == 'report_run_stage':
            # the server is about to run specified job.
            # if the handle return True, it will continue
            # if false, it will cancel the job
            task_id = data.get('task_id')
            envid = data.get('envid')
            stage = data.get('stage')
            if (task_id is None) or (envid is None) or (stage is None):
                return rc.BAD_REQUEST
            
            return self.report_run_stage(server_id, task_id, envid, stage)
        
        elif command == 'job_finished':
            # the server finished the job
            task_id = data.get('task_id')
            if task_id is None:
                return rc.BAD_REQUEST
            
            return self.job_finished(server_id, task_id)
        
        elif command == 'job_error':
            # the server finished the job
            task_id = data.get('task_id')
            error_log = data.get('error_log')
            if task_id is None or (error_log is None):
                return rc.BAD_REQUEST
            
            return self.job_error(server_id, task_id, error_log)
    
    def confirm_run(self, server_id, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return rc.NOT_FOUND
        except ValueError:
            return rc.BAD_REQUEST
        
        if task.get_status() == 'pending':
            try:
                queue = task.queue
            except TaskQueue.DoesNotExist:
                # No task queue, don't allow run
                return False
            if queue.server_id == server_id:
                # This task is indeed scheduled to run on this server
                queue.status = 'running'
                queue.save()
                return True
            return False
        else:
            return False
    
    def report_run_stage(self, server_id, task_id, envid, stage):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return rc.NOT_FOUND
        except ValueError:
            return rc.BAD_REQUEST
        
        if task.get_status() == 'running':
            try:
                queue = task.queue
            except TaskQueue.DoesNotExist:
                # No task queue, don't allow run
                return False
            if queue.server_id == server_id:
                # This task is indeed scheduled to run on this server
                queue.stage = stage
                queue.envid = envid
                queue.save()
                return True
            return False
        else:
            return False
    
    def job_finished(self, server_id, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return rc.NOT_FOUND
        except ValueError:
            return rc.BAD_REQUEST
        
        if task.get_status() == 'running':
            try:
                queue = task.queue
            except TaskQueue.DoesNotExist:
                # No task queue, this command must be invalid
                return False
            if queue.server_id == server_id:
                # This task is indeed scheduled to run on this server
                queue.status = 'finished'
                queue.is_error = False
                queue.error_log = ''
                queue.save()
                return True
            return False
        else:
            return False
    
    def job_error(self, server_id, task_id, error_log):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return rc.NOT_FOUND
        except ValueError:
            return rc.BAD_REQUEST
        
        if task.get_status() == 'running':
            try:
                queue = task.queue
            except TaskQueue.DoesNotExist:
                # No task queue, this command must be invalid
                return False
            if queue.server_id == server_id:
                # This task is indeed scheduled to run on this server
                queue.status = 'finished'
                queue.is_error = True
                queue.error_log = error_log
                queue.save()
                return True
            return False
        else:
            return False
    
    def retrieve_job(self, server_id):
        ''' Return task id '''
        queuelist = TaskQueue.objects.filter(server=None, status='pending')
        if queuelist.count() == 0:
            return rc.BAD_REQUEST
        
        queue = queuelist[0]
        queue.server_id = server_id
        queue.save()
        return queue.task_id


class GradsWRFHandler(BaseHandler):
    ''' Get list of grads plot. '''
    methods_allowed = ('GET',)
    
    def read(self, request, server_id=None, envid=None, domain=None):
        from aqm_utils import server as rpcserver
        
        if server_id is None:
            server_id = request.GET.get('server_id')
        if envid is None:
            envid = request.GET.get('envid')
        if domain is None:
            domain = request.GET.get('domain')
        
        if not all((server_id, envid, domain)):
            return rc.BAD_REQUEST
        
        c = rpcserver.rpc_client(server_id=server_id)
        plot_rel_list = c.wrf.get_plot(int(envid), int(domain))
        plot_list = []
        
        for p in plot_rel_list:
            args = urllib.urlencode({'f': p})
            url = '%s?%s' % (reverse('grads-wrf-plot', None, [server_id, envid]), args)
            filename = os.path.basename(p)
            fname, ext = os.path.splitext(filename)
            c = fname.split('_')
            description = fname
            
            if len(c) == 3:
                time_el = c[2].split(':')
                if len(time_el) == 4:
                    description = '%s-%s-%s %s:00' %(time_el[2], time_el[1], time_el[0], time_el[3])
                
            plot_list.append({'url': url, 'description': description})
        
        return plot_list
    
    def create(self, request, *args, **kwargs):
        return rc.FORBIDDEN
    
    def update(self, request, *args, **kwargs):
        return rc.FORBIDDEN
    
    def delete(self, request, *args, **kwargs):
        return rc.FORBIDDEN
    