
# setup automatic update of every server in the given list
window.setup_server_list_auto_update = (server_list, interval) ->
    setup_server_auto_update server, interval for server in server_list
    
# setup automatic update of a given server
setup_server_auto_update = (server, interval) ->
    updater = (server) ->
        $.ajax {url: server.get_status_rest_url,
        dataType: "json",
        type: "GET",
        success: update_server,
        error: (jqXHR, textStatus, errorThrown) ->
            console.log errorThrown, jqXHR
            if jqXHR.status == 0
                $("#server_#{ server.id } > .header > .label.status").text("check your internet connection")
            else if jqXHR.status == 404
                $("#server_#{ server.id } > .header > .label.status").text("server does not exist")
            else if jqXHR.status == 500
                $("#server_#{ server.id } > .header > .label.status").text("internal web server error")
            else if jqXHR.status == 503
                $("#server_#{ server.id } > .header > .label.status").text("service disruption")
            
            $("#server_#{ server.id } > .header > .label.status").removeClass("label-success").addClass("label-important")
            simplebar.set("#cpu-usage-server-#{ server.id }", 0, "--")
            simplebar.set("#memory-usage-server-#{ server.id }", 0, "--")
            simplebar.set("#disk-usage-server-#{ server.id }", 0, "--")
            simplebar.set("#slot-usage-server-#{ server.id }", 0, "--")
        }
        
    
    timer = setInterval ()->
        updater server
    , interval


# update server details screen
update_server = (server_stat) ->
    #console.log "#cpu-usage-server-#{ server_stat.id }", server_stat
    simplebar.set("#cpu-usage-server-#{ server_stat.id }", server_stat.cpu, "#{ server_stat.cpu }%")
    
    memory_used = Math.round(server_stat.memory_used / (1024 * 1024))
    memory_total = Math.round(server_stat.memory_total / (1024 * 1024))
    memory_label =  "#{ memory_used } MB / #{ memory_total } MB"
    simplebar.set("#memory-usage-server-#{ server_stat.id }", server_stat.memory_percent, memory_label)
    
    disk_used = Math.round(server_stat.disk_used / (1024 * 1024 * 1024))
    disk_total = Math.round(server_stat.disk_total / (1024 * 1024 * 1024))
    disk_label = "#{ disk_used } GB / #{ disk_total } GB"
    simplebar.set("#disk-usage-server-#{ server_stat.id }", server_stat.disk_percent, disk_label)
    
    slot_percent = (server_stat.slot_used / server_stat.slot_total) * 100
    slot_label = "#{ server_stat.slot_used } of #{ server_stat.slot_total }"
    simplebar.set("#slot-usage-server-#{ server_stat.id }", slot_percent, slot_label)
    
    $("#server_#{ server_stat.id } > .header > .label.status").text("healthy")
    $("#server_#{ server_stat.id } > .header > .label.status").removeClass("label-important").addClass("label-success")
	
    