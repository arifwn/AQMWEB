
import numbers

from django.db import IntegrityError

from aqm_utils.xmlrpc import Client
from aqm_web.models import Server

from wrf.models import Task, TaskQueue


def run_task(task_id):
    ''' Queued task to be run by rpc server. '''
    # read the task
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {'success': False, 'message': 'Task does not exist.'}
    
    data = {}
    data['task_id'] = task_id
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
        
        # TODO: uncomment this when ready to test!
        target_server_client.wrf.add_job(data)
        
        # now what left is to wait for RPC server update TaskQueue item with
        # env_id from rpc server environment
        # if the task queue already deleted when rpc server start processing
        # the task, rpc server will cancel executing the task
        
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

def rerun_task(task_id):
    ''' Queued task to be run by rpc server again from the first stage. '''
    # read the task
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
    
    # check the task queue
    try:
        target_server = task.queue.server
    except TaskQueue.DoesNotExist:
        return {'success': False, 'message': 'Queued Task does not exist. Please use "run" instead of "rerun" command.'}
    
    use_another_server = True
    
    # if the queued task already assigned to a server an has env_id,
    # use that server again
    if task.queue.envid is not None:
        if target_server is not None:
            target_server_client = Client('https://%s:%d' % (target_server.address, target_server.port))
            try:
                status = target_server_client.server.utilization()
                use_another_server = False
                # this task will be queued to this server IMMEDIATELY
                # even if server task slot is full, this task will be pushed
                # to rpcserver's internal queue
            except:
                # cannot connect to this server. use another server.
                use_another_server = True
    
    if use_another_server:
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
    
    
    # reset the queued task
    jobqueue = task.queue
    jobqueue.status = 'pending'
    jobqueue.stage = ''
    jobqueue.is_error = False
    jobqueue.error_log = ''
    if use_another_server:
        jobqueue.envid = None
        jobqueue.server = target_server
    
    try:
        jobqueue.save()
    except IntegrityError:
        # Error: task already queued or run
        # use rerun instead of run
        status = {'success': False,
                  'message': 'Cannot save the task queue!'}
        return status
    
    if target_server is not None:
        # give this server a job
        
        # TODO: uncomment this when ready to test!
        # target_server_client.wrf.add_job(data)
        
        # now what left is to wait for RPC server update TaskQueue item with
        # env_id from rpc server environment
        # if the task queue already deleted when rpc server start processing
        # the task, rpc server will cancel executing the task
        
        status = {'success': True,
                  'message': 'Task queued to server. Waiting for update from RPC Server.'}
        return status
    else:
        # no server has empty slot, add the task to queue list
        # rpc server must poll the web interface for queued job
        
        status = {'success': True,
                  'message': 'Task queued to server. Waiting to be picked by an RPC Server.'}
        return status

def stop_task(task_id):
    ''' Stop task currently run by rpc server. '''
    # read the task
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {'success': False, 'message': 'Task does not exist.'}
    
    target_server = None
    target_server_client = None
    
    # check the task queue
    try:
        target_server = task.queue.server
    except TaskQueue.DoesNotExist:
        return {'success': False, 'message': 'Queued Task does not exist.'}
    
    taskqueue = task.queue
    target_server_client = Client('https://%s:%d' % (target_server.address,
                                                     target_server.port))
    
    try:
        if target_server_client.wrf.stop_job(taskqueue.envid):
            taskqueue.status = 'canceled'
            taskqueue.save()
            return {'success': True, 'message': ''}
        else:
            return {'success': False, 'message': 'Cannot stop specified task.'}
    except Exception, e:
        return {'success': False, 'message': 'Cannot stop specified task. RPC Fault: %s' % e}

def cancel_task(task_id):
    ''' Cancel queued task. '''# read the task
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {'success': False, 'message': 'Task does not exist.'}
    
    target_server = None
    target_server_client = None
    
    # check the task queue
    try:
        target_server = task.queue.server
    except TaskQueue.DoesNotExist:
        return {'success': False, 'message': 'Queued Task does not exist.'}
    
    taskqueue = task.queue
    
    if target_server is not None:
        if taskqueue.status == 'running':
            return {'success': False, 'message': 'Task is running. Use "Stop" instead of "Cancel" command. Refresh page if necessary.'}
        
    taskqueue.status = 'canceled'
    taskqueue.save()
    return {'success': True, 'message': ''}

def retry_task(task_id):
    ''' Queued task to be run by rpc server from last running stage '''
    status = {'success': False, 'message': 'Not Implemented!'}
    return status
