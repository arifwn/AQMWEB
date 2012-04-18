
window.render_result_browser = (target_id, data_list) ->
    $("#{ target_id } .viewport .viewlist").empty()
    
    i = 1
    for data in data_list
        html = """<li data-item-description="#{ data.description }" data-stream-gallery-num="#{ i }">
                    <img class="view-item" src="#{ data.url }" />
                </li>"""
        $("#{ target_id } .viewport .viewlist").append html
        i += 1
    
    