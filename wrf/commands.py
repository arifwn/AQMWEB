
import numbers

from django.db import IntegrityError

from aqm_utils.xmlrpc import Client
from aqm_web.models import Server

from wrf.models import Task, TaskQueue


def run_task(task_id):
    ''' Queued task to be run by rpc server. '''
    
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {'success': False, 'message': 'Task does not exist.'}
    
    data = {}
    data['id'] = task_id
    data['name'] = task.name
    data['WRFnamelist'] = task.setting.namelist_wrf
    data['WPSnamelist'] = task.setting.namelist_wps
    data['ARWpostnamelist'] = task.setting.namelist_arwpost
    data['grads_template'] = task.setting.grads_template
    
    target_server = None
    target_server_client = None
    
    # loop over available server and see if one has empty task slot
    for server in Server.objects.filter(is_enabled=True).all():
        server_addr = 'https://%s:%d' % (server.address, server.port)
        c = Client(server_addr)
        try:
            status = c.server.utilization()
        except:
            # cannot connect to this server. continue to the next one
            continue
        
        slot_used = status.get('slot_used')
        slot_total = status.get('slot_total')
        if (not isinstance(slot_used, numbers.Number)) or (not isinstance(slot_total, numbers.Number)):
            # something is wrong with the returned data
            # continue to the next server
            continue
        
        if slot_used < slot_total:
            # this server has available slot.
            target_server = server
            target_server_client = c
            break
    
    if target_server is not None:
        # give this server a job
        # target_server_client.wrf.add_job(data)
        
        jobqueue = TaskQueue(task=task,
                             server=target_server,
                             status='pending')
        try:
            jobqueue.save()
        except IntegrityError:
            # Error: task already queued or run
            # use rerun instead of run
            status = {'success': False,
                      'message': 'Task already assigned to a server. Please use "rerun" instead of "run" command.'}
            return status
        
        # now what left is to wait for RPC server update TaskQueue item with
        # env_id from rpc server environment
        
        status = {'success': True,
                  'message': 'Task queued to server. Waiting for update from RPC Server.'}
        return status
    else:
        # no server has empty slot, add the task to queue list
        # rpc server must poll the web interface for queued job
        
        jobqueue = TaskQueue(task=task,
                             status='pending')
        try:
            jobqueue.save()
        except IntegrityError:
            # Error: task already queued or run
            # use rerun instead of run
            status = {'success': False,
                      'message': 'Task already assigned to a server. Please use "rerun" instead of "run" command.'}
            return status
        
        status = {'success': True,
                  'message': 'Task queued to server. Waiting to be picked by an RPC Server.'}
        return status
    

def retry_task(task_id):
    ''' Queued task to be run by rpc server from last running stage '''
    status = {'success': False, 'message': 'Not Implemented!'}
    return status

def rerun_task(task_id):
    ''' Queued task to be run by rpc server again from the first stage. '''
    status = {'success': False, 'message': 'Not Implemented!'}
    return status

def stop_task(task_id):
    ''' Stop task currently run by rpc server. '''
    status = {'success': False, 'message': 'Not Implemented!'}
    return status

def cancel_task(task_id):
    ''' Cancel queued task. '''
    status = {'success': False, 'message': 'Not Implemented!'}
    return status
