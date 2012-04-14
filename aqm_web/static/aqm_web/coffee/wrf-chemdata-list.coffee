
# append all task in the given list to the target
window.render_chemdata_list = (target, chemdata_list) ->
    #console.log task_list
    append_chemdata target, chemdata for chemdata in chemdata_list

# append a task html to the end of the target
append_chemdata = (target, chemdata) ->
    chemdata_html = get_chemdata_html chemdata
    html = """
    <li id="chemdata-#{ chemdata.id }">
        #{ chemdata_html }
    </li>
    """
    $(target).append html
    
# construct a html snippet from a given chemdata
get_chemdata_html = (chemdata) ->
    html = """
    <div class="header">
        <h2><a href="#">#{ chemdata.name }</a></h2>
    </div>
    <div class="content">
        <div class="well">
        #{ chemdata.description }
        </div>
        <table class="table table-striped table-bordered table-condensed">
            <thead>
                <tr>
                    <th>User</th>
                    <th>Uploaded</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><a href="/accounts/profile/#{ chemdata.user.username }"><img class="avatar" src="/accounts/avatar/t32x32/#{ chemdata.user.username }" width="32" height="32" style="height: 32px;" /></a> <a href="/accounts/profile/#{ chemdata.user.username }">#{ chemdata.user.get_full_name } (#{ chemdata.user.username })</a></td>
                    <td>#{ chemdata.created }</td>
                </tr>
            </tbody>
        </table>
        <ul class="controls">
            <li><a class="btn btn-success" href="#"><i class="icon-th-list icon-white"></i> Details</a></li>
            <li><a class="btn" href="#{ chemdata.edit_url }"><i class="icon-edit"></i> Edit</a></li>
            <li><a class="btn btn-danger" href="#"><i class="icon-remove icon-white"></i> Remove</a></li>
        </ul>
    </div>
    """