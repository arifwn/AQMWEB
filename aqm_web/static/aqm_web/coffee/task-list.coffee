
# append all task in the given list to the target
window.render_task_list = (target, task_list) ->
    console.log task_list
    append_task target, task for task in task_list

# update displayed html with data from a given task
window.update_task = (task) ->
    # console.log "updating task-#{ task.id }", task
    task_html = get_task_html task
    $("#task-#{ task.id }").empty()
    $("#task-#{ task.id }").append task_html

# setup automatic update of every task in the given list
window.setup_task_list_auto_update = (task_list, interval) ->
    setup_task_auto_update task, interval for task in task_list

# setup automatic update of a given task
setup_task_auto_update = (task, interval) ->
    updater = (task) ->
        $.ajax {url: task.get_rest_url,
        dataType: "json",
        type: "GET",
        success: update_task,
        error: (jqXHR, textStatus, errorThrown) ->
            console.log errorThrown
        }
        
    
    timer = setInterval ()->
        updater task
    , interval

# append a task html to the end of the target
append_task = (target, task) ->
    task_html = get_task_html task
    html = """
    <li id="task-#{ task.id }">
        #{ task_html }
    </li>
    """
    $(target).append html

# construct a html snippet from a given task
get_task_html = (task) ->
    controls_html = ""
    progress_html = ""
    
    if task.get_status == "draft"
        controls_html = """
        <li><a class="btn btn-info" href="#">Run</a></li>
        <li><a class="btn" href="#">Details</a></li>
        <li><a class="btn" href="#">Edit</a></li>
        <li><a class="btn btn-danger" href="#">Delete</a></li>
        """
        
        progress_html = """
        <div class="counter">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label">draft</span></div>
        """
        
    else if task.get_status == "pending"
        controls_html = """
        <li><a class="btn btn-danger" href="#">Cancel</a></li>
		<li><a class="btn" href="#">Details</a></li>
        """
        
        progress_html = """
        <div class="counter warning">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-warning">pending</span></div>
        """
        
    else if task.get_status == "running"
        controls_html = """
        <li><a class="btn btn-danger" href="#">Stop</a></li>
		<li><a class="btn" href="#">Details</a></li>
        """
        
        progress_html = """
        <div class="counter info">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-info">running</span></div>
        <div class="progress progress-striped active">
            <div class="bar" style="width: 30%;"></div>
        </div>
        """
        
    else if task.get_status == "finished"
        controls_html = """
        <li><a class="btn btn-success" href="#">Results</a></li>
        <li><a class="btn btn-info" href="#">Run Again</a></li>
        <li><a class="btn" href="#">Details</a></li>
        <li><a class="btn" href="#">Edit</a></li>
        <li><a class="btn btn-danger" href="#">Delete</a></li>
        """
        
        progress_html = """
        <div class="counter success">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-success">finished</span></div>
        """
        
    else if task.get_status == "error"
        controls_html = """
        <li><a class="btn btn-info" href="#">Retry last stage</a></li>
        <li><a class="btn btn-info" href="#">Run</a></li>
        <li><a class="btn" href="#">Details</a></li>
        <li><a class="btn" href="#">Edit</a></li>
        <li><a class="btn btn-danger" href="#">Delete</a></li>
        """
        
        progress_html = """
        <div class="counter important">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-important">error</span></div>
        """
        
    else if task.get_status == "canceled"
        controls_html = """
        <li><a class="btn btn-info" href="#">Resume from last stage</a></li>
        <li><a class="btn btn-info" href="#">Run</a></li>
        <li><a class="btn" href="#">Details</a></li>
        <li><a class="btn" href="#">Edit</a></li>
        <li><a class="btn btn-danger" href="#">Delete</a></li>
        """
        
        progress_html = """
        <div class="counter important">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-important">canceled</span></div>
        """
    
    html = """
    <div class="header">
        <h2><a href="#">#{ task.name }</a></h2>
    </div>
    <div class="content">
        <div class="well">
        #{ task.description }
        </div>
        <table class="table table-striped table-bordered table-condensed">
            <thead>
                <tr>
                    <th>User</th>
                    <th>Domain</th>
                    <th>Period</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><a href="/accounts/profile/#{ task.user.username }"><img class="avatar" src="/accounts/avatar/t32x32/#{ task.user.username }" width="32" height="32" style="height: 32px;" /></a> <a href="/accounts/profile/#{ task.user.username }">#{ task.user.get_full_name } (#{ task.user.username })</a></td>
                    <td>#{ task.setting.get_max_dom }</td>
                    <td>#{ task.setting.get_start_date } &mdash; #{ task.setting.get_end_date }</td>
                </tr>
            </tbody>
        </table>
        <ul class="controls">
            #{ controls_html }
        </ul>
    </div>
    
    <div class="task-progress">
        #{ progress_html }
    </div>
    """