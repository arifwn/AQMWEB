
window.task_list_timers = []
window.task_list_data = []
window.task_command_url = ''

# clear auto update timer
window.reset_task_list = (target) ->
    # reset update timer
    clearInterval timer for timer in window.task_list_timers
    window.task_list_timers = []
    
    # reset filter button
    $(".toolbox .nav > li").removeClass "active"
    $("#filter-all").parent().addClass "active"
    
    loading_html = """
    <li>
        <div class="alert alert-info">
            <p><img src="#{ static_url }aqm_web/img/spinner.gif" alt="Loading..."></p>
        </div>
    </li>
    """
    
    $(target).empty()
    $(target).append loading_html
    
    

# append all task in the given list to the target
window.render_task_list = (target, task_list) ->
    #console.log task_list
    window.task_list_data = task_list
    append_task target, task for task in task_list

# reinstall button event handler
window.reinit_event_handler = (task)->
    # run
	$("#task-#{ task.id } .control-run").click (e) ->
		button = this
		task_command 'run', task, button
        
    # rerun
	$("#task-#{ task.id } .control-rerun").click (e) ->
		button = this
		task_command 'rerun', task, button
        
    # retry
	$("#task-#{ task.id } .control-retry").click (e) ->
		button = this
		task_command 'retry', task, button
        
    # stop
	$("#task-#{ task.id } .control-stop").click (e) ->
		button = this
		task_command 'stop', task, button
        
    # cancel
	$("#task-#{ task.id } .control-cancel").click (e) ->
		button = this
		task_command 'cancel', task, button
        

# update displayed html with data from a given task
window.update_task = (task) ->
    # console.log "updating task-#{ task.id }", task
    task_html = get_task_html task
    $("#task-#{ task.id }").empty()
    $("#task-#{ task.id }").append task_html
    window.reinit_event_handler task

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
        
    
    real_interval = 0
    if task.get_status == "running"
        # if it currently running, update at full speed
        real_interval = interval
    else if task.get_status == "running"
        # if it pending, don't update as fast
        real_interval = 3 * interval
    else
        # no need for speedy update
        real_interval = 10 * interval
    
    timer = setInterval ()->
        updater task
    , real_interval
    
    window.task_list_timers.push timer

# append a task html to the end of the target
append_task = (target, task) ->
    task_html = get_task_html task
    html = """
    <li id="task-#{ task.id }">
        #{ task_html }
    </li>
    """
    $(target).append html
    window.reinit_event_handler task

# construct a html snippet from a given task
get_task_html = (task) ->
    controls_html = ""
    progress_html = ""
    
    if task.get_status == "draft"
        controls_html = """
        <li><button class="btn btn-info control-run" data-loading-text="Run" autocomplete="off"><i class="icon-play icon-white"></i> Run</button></li>
        <li><a class="btn" href="#{ task.get_url }"><i class="icon-th-list"></i> Details</a></li>
        <li><a class="btn" href="#"><i class="icon-edit"></i> Edit</a></li>
        <li><a class="btn btn-danger" href="#"><i class="icon-remove icon-white"></i> Delete</a></li>
        """
        
        progress_html = """
        <div class="counter">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label">draft</span></div>
        """
        
    else if task.get_status == "pending"
        controls_html = """
        <li><button class="btn btn-danger control-cancel" data-loading-text="Cancel" autocomplete="off"><i class="icon-remove-sign icon-white"></i> Cancel</button></li>
		<li><a class="btn" href="#{ task.get_url }"><i class="icon-th-list"></i> Details</a></li>
        """
        
        progress_html = """
        <div class="counter warning">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-warning">pending</span></div>
        """
        
    else if task.get_status == "running"
        controls_html = """
        <li><button class="btn btn-danger control-stop" data-loading-text="Stop" autocomplete="off"><i class="icon-stop icon-white"></i> Stop</button></li>
		<li><a class="btn" href="#{ task.get_url }"><i class="icon-th-list"></i> Details</a></li>
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
        <li><button class="btn btn-info control-rerun" data-loading-text="Run Again" autocomplete="off"><i class="icon-repeat icon-white"></i> Run Again</button></li>
        <li><a class="btn" href="#{ task.get_url }"><i class="icon-th-list"></i> Details</a></li>
        <li><a class="btn" href="#"><i class="icon-edit"></i> Edit</a></li>
        <li><a class="btn btn-danger" href="#"><i class="icon-remove icon-white"></i> Delete</a></li>
        """
        
        progress_html = """
        <div class="counter success">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-success">finished</span></div>
        """
        
    else if task.get_status == "error"
        controls_html = """
        <li><button class="btn btn-info control-retry" data-loading-text="Retry last stage" autocomplete="off"><i class="icon-refresh icon-white"></i> Retry last stage</button></li>
        <li><button class="btn btn-info control-rerun" data-loading-text="Run Again" autocomplete="off"><i class="icon-repeat icon-white"></i> Run Again</button></li>
        <li><a class="btn" href="#{ task.get_url }"><i class="icon-th-list"></i> Details</a></li>
        <li><a class="btn" href="#"><i class="icon-edit"></i> Edit</a></li>
        <li><a class="btn btn-danger" href="#"><i class="icon-remove icon-white"></i> Delete</a></li>
        """
        
        progress_html = """
        <div class="counter important">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-important">error</span></div>
        """
        
    else if task.get_status == "canceled"
        controls_html = """
        <li><button class="btn btn-info control-retry" data-loading-text="Resume from last stage" autocomplete="off"><i class="icon-refresh icon-white"></i> Resume from last stage</button></li>
        <li><button class="btn btn-info control-rerun" data-loading-text="Run Again" autocomplete="off"><i class="icon-repeat icon-white"></i> Run Again</button></li>
        <li><a class="btn" href="#{ task.get_url }"><i class="icon-th-list"></i> Details</a></li>
        <li><a class="btn" href="#"><i class="icon-edit"></i> Edit</a></li>
        <li><a class="btn btn-danger" href="#"><i class="icon-remove icon-white"></i> Delete</a></li>
        """
        
        progress_html = """
        <div class="counter important">#{ task.get_progress_percent }%</div>
        <div class="stage">#{ task.get_stage }</div>
        <div><span class="label label-important">canceled</span></div>
        """
    
    html = """
    <div class="header">
        <h2><a href="#{ task.get_url }">#{ task.name }</a></h2>
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
                    <td>#{ task.setting.max_dom }</td>
                    <td>#{ task.setting.start_date } &mdash; #{ task.setting.end_date }</td>
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

# display all task
window.filter_display = (task_list, filter) ->
    $(".toolbox .nav > li").removeClass "active"
    $("#filter-#{ filter }").parent().addClass "active"
    $('html, body').animate {scrollTop: 0}, 300
    
    #console.log "#filter-#{ filter }", window.task_list_data
    
    filter_display = (task) ->
        if filter == "all"
            $("#task-#{ task.id }").removeClass "hidden"
        else
            if task.get_status == filter
                $("#task-#{ task.id }").removeClass "hidden"
            else
                $("#task-#{ task.id }").addClass "hidden"
    
    filter_display task for task in window.task_list_data

# perform command to a task
window.task_command = (command, task, button) ->
    console.log command
    $(button).button('loading')
    
    $.ajax {url: window.task_command_url,
    dataType: "json",
    type: "POST",
    data: {task_id: task.id, command: command},
    success: (data)->
        $(button).button('reset')
        if data.success
            # update the task display
            $.ajax {url: task.get_rest_url,
            dataType: "json",
            type: "GET",
            success: update_task
            }
            # TODO: reinit the update timer according to newly aquired task status
            # obtain new task list
            $.ajax {url: window.task_list_url,
            dataType: "json",
            type: "GET",
            success: (data) ->
                # reset update timer
                clearInterval timer for timer in window.task_list_timers
                window.task_list_timers = []
                window.task_list_data = data
                # setup auto update
                window.setup_task_list_auto_update(data, 5000)
                console.log "timer updated!"
            }
            
            console.log "operation succeed!"
        else
            window.aqm.alert "Error", data.message
    ,
    error: (jqXHR, textStatus, errorThrown) ->
        $(button).button('toggle')
        window.aqm.alert "Error", "Connection Failed: #{ textStatus } #{ errorThrown }"
    }
    