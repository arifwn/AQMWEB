
def run_task(task_id):
    ''' Queued task to be run by rpc server. '''
    return False

def retry_task(task_id):
    ''' Queued task to be run by rpc server from last running stage '''
    return False

def rerun_task(task_id):
    ''' Queued task to be run by rpc server again from the first stage. '''
    return False

def stop_task(task_id):
    ''' Stop task currently run by rpc server. '''
    return False

def cancel_task(task_id):
    ''' Cancel queued task. '''
    return False
