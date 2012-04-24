
window.render_result_browser = (target_id, data_list) ->
    $("#{ target_id } .viewport .viewlist").empty()
    
    i = 1
    for data in data_list
        html = """<li data-item-description="#{ data.description }" data-stream-gallery-num="#{ i }">
                    <img class="view-item" src="#{ data.url }" />
                </li>"""
        $("#{ target_id } .viewport .viewlist").append html
        i += 1

# update WRF log display
window.update_log_wrf = (task_id) ->
    real_log = 'just "test"'
    real_log_html = prettyPrintOne(real_log, 'js', true);
    $('#real-exe-log').empty();
    $('#real-exe-log').append(real_log_html);
    
    wrf_log = 'just "test"'
    wrf_log_html = prettyPrintOne(wrf_log, 'js', true);
    $('#wrf-exe-log').empty();
    $('#wrf-exe-log').append(wrf_log_html);
    
    
    