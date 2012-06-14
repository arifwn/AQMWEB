
$(document).ready(() ->
    # Script entry point
    
    # Coordinate Settings
    # only display relevant location field based on selected projection type
    $('#ntf-proj').change((e) ->
        e.preventDefault()
        proj = $('#ntf-proj').val()
        show_location_fields(proj)
    )
    show_location_fields($('#ntf-proj').val())
    
    # location preview
    $('#btn-map-preview').click((e) ->
        e.preventDefault()
        latitude = get_float('#ntf-ref-lat', '#ntf-ref-container')
        longitude = get_float('#ntf-ref-lon', '#ntf-ref-container')
        
        if isNaN(latitude) or isNaN(longitude)
            return
        else
            true_lat = Math.abs(latitude)
            # update true latitude field if it's empty
            if isNaN(get_float('#ntf-true-lat1'))
                $('#ntf-true-lat1').val(true_lat)
            
            show_preview_map(latitude, longitude)
    )
    
    # close location preview
    $('#btn-area-modal-close').click((e) ->
        e.preventDefault()
        $('#area-modal').modal('hide')
    )
    
    # map preview modal on hide event
    $('#area-modal').on('hidden', () ->
        spinner_func.spinner_stop('#map-loading-spinner')
    )
    
    
    # Domain Settings
    
    # initialize domain list
    window.aqm.domain_list = []
    
    # initialize domain id
    window.aqm.domain_last_id = 0
    
    # add domain button
    $('#btn-add-domain').click((e) ->
        e.preventDefault()
        reset_domain_modal()
        show_parent_ij_field($('#ntf-parent-domain').val())
        $('#domain-modal').modal('show')
    )
    
    # display i_parent_start and j_parent_start depending on parent selection
    $('#ntf-parent-domain').change((e) ->
        e.preventDefault()
        show_parent_ij_field($('#ntf-parent-domain').val())
        
    )
    
    # domain modal window save button
    $('#btn-domain-modal-ok').click((e) ->
        e.preventDefault()
        
        # add or edit the domain
        if save_domain($('#domain-modal').attr('data-domain-id'))
            $('#domain-modal').modal('hide')
        else
            window.alert "Please check your input!"
    )
    
    # close domain modal window
    $('#btn-domain-modal-cancel').click((e) ->
        e.preventDefault()
        $('#domain-modal').modal('hide')
    )
    
    # init test data
    init_test_data()
    
    render_domain_list()
)

render_domain_list = () ->
    # remove existing rows
    $('#domain-list tr[data-domain-listing]').remove()
    
    # render all domain it the table
    render_domain domain for domain in window.aqm.domain_list

render_domain = (domain) ->
    parent_domain = get_domain domain.parent_id
    parent_domain_name = '--'
    if parent_domain?
        parent_domain_name = parent_domain.name
    $('#domain-list > tbody:last').append """<tr data-domain-listing="listing"><td><input type="checkbox" data-domain-id="#{ domain.id }"></td><td><a href="#" class="domain_link_edit" data-domain-id="#{ domain.id }">#{ domain.name }</a></td><td>#{ parent_domain_name }</td><td>#{ domain.width }</td><td>#{ domain.height }</td><td>#{ domain.dx }</td><td>#{ domain.dy }</td></tr>"""

get_domain = (domain_id) ->
    # return domain object from global list
    return domain for domain in window.aqm.domain_list when domain.id == domain_id

init_test_data = () ->
    # test data for debugging purpose
    
    width = 50
    height = 50
    dx = 9000
    dy = 9000
    ratio = 1
    parent_id = 0
    i_parent_start = 0
    j_parent_start = 0
    
    name = 'Test Domain 1'
    domain1 = new Domain name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start
    domain1.assign_id()
    
    name = 'Test Domain 2'
    dx = 3000
    dy = 3000
    ratio = 3
    parent_id = domain1.id
    i_parent_start = 25
    j_parent_start = 25
    domain2 = new Domain name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start
    domain2.assign_id()
    
    name = 'Test Domain 3'
    dx = 3000
    dy = 3000
    ratio = 3
    parent_id = domain2.id
    i_parent_start = 25
    j_parent_start = 25
    domain3 = new Domain name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start
    domain3.assign_id()
    
    window.aqm.domain_list.push domain1
    window.aqm.domain_list.push domain2
    window.aqm.domain_list.push domain3

save_domain = (domain_id) ->
    domain_id = parseInt(domain_id)
    
    if isNaN(domain_id)
        console.log 'add new domain'
        return add_domain()
    else
        console.log 'edit existing domain'
        return false

add_domain = () ->
    name = $('#ntf-dom-name').val()
    width = $('#ntf-dom-width').val()
    height = $('#ntf-dom-height').val()
    dx = $('#ntf-dom-dx').val()
    dy = $('#ntf-dom-dy').val()
    ratio = $('#ntf-ratio').val()
    parent_id = $('#ntf-parent-domain').val()
    i_parent_start = $('#ntf-dom-parent-start-i').val()
    j_parent_start = $('#ntf-dom-parent-start-j').val()
    domain = new Domain name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start
    
    if domain.check_all()
        domain.assign_id()
        window.aqm.domain_list.push domain
        return true
    else
        return false

show_parent_ij_field = (parent_domain) ->
    # if parent_domain is '0', hide parent i j position fields, and vice versa
    parent_id = parseInt(parent_domain)
    
    if parent_id == 0
        $('#ntf-dom-parent-start-container').hide()
    else
        $('#ntf-dom-parent-start-container').show()

reset_domain_modal = () ->
    # reset fields on domain modal window
    title = 'Add New Domain'
    $('#ntf-parent-domain').val(0)
    $('#domain-modal .clearfix').removeClass('error')
    $('#domain-modal .input-prepend').removeClass('error')
    $('#domain-modal .modal-header h3').text(title)
    $('#ntf-dom-name').val('')
    $('#ntf-dom-id').val('')
    $('#ntf-dom-width').val('')
    $('#ntf-dom-height').val('')
    $('#ntf-dom-dx').val('')
    $('#ntf-dom-dy').val('')
    $('#ntf-ratio').val('')
    $('#ntf-dom-parent-start-i').val('')
    $('#ntf-dom-parent-start-j').val('')
    
    $('#ntf-parent-domain').html ''
    $('#ntf-parent-domain').append '<option selected value="0">-- None --</option>'
    
    append_parent_dropdown_list domain for domain in window.aqm.domain_list
    
    # set mode to 'add'
    $('#domain-modal').attr('data-domain-id', '0')

append_parent_dropdown_list = (domain) ->
    $('#ntf-parent-domain').append "<option value=\"#{ domain.id }\">#{ domain.name }</option>"

show_preview_map = (latitude, longitude) ->
    # show a modal dialog showing a map with marker on specified lat & lon
    true_lat = Math.abs(latitude)
    
    upper_lat = latitude + 20
    upper_lon = longitude + 27
    lower_lat = latitude - 20
    lower_lon = longitude - 27
    
    if upper_lat > 80
        upper_lat = 80
        lower_lat = 80 - 40
    
    if lower_lat < -80
        lower_lat = -80
        upper_lat = -80 + 40
    
    map_url = "#{ window.aqm.map_mercator_base_url }?upper_lat=#{ upper_lat }&upper_lon=#{ upper_lon }&lower_lat=#{ lower_lat }&lower_lon=#{ lower_lon }&true_lat=#{ true_lat }&ref_lat=#{ latitude }&ref_lon=#{ longitude }"
    show_map_modal map_url

show_map_modal = (map_url) ->
    # show a modal window displaying specified map url
    spinner_func.spinner_play('#map-loading-spinner')
    
    $('#area-modal .preview-image').hide().load(() ->
        $(this).fadeIn()
        
    ).attr('src', map_url)
    $('#area-modal').modal('show')

get_float = (source, container='') ->
    # attemp to get a float from source element.
    # on success remove error class from container and vice versa
    val = parseFloat $(source).val()
    if isNaN(val)
        $(container).addClass 'error'
    else
        $(container).removeClass 'error'
    return val


show_location_fields = (projection) ->
    # show relevant location fields based on selected projection type
    switch projection
        when "mercator" then show_mercator_fields()
        when "lambert" then show_lambert_fields()
        when "polar" then show_polar_fields()
        when "lat-lon" then show_latlon_fields()


show_mercator_fields = () ->
    # show location fields for mercator projection
    console.log "mercator selected"
    $('#ntf-true-lat1-cont').show()
    $('#ntf-true-lat2-cont').hide()
    $('#ntf-stand-lon-cont').hide()
    $('#ntf-pole-lat-cont').hide()
    $('#ntf-pole-lon-cont').hide()

show_lambert_fields = () ->
    # show location fields for lambert conformal projection
    console.log "lambert selected"
    $('#ntf-true-lat1-cont').show()
    $('#ntf-true-lat2-cont').show()
    $('#ntf-stand-lon-cont').show()
    $('#ntf-pole-lat-cont').hide()
    $('#ntf-pole-lon-cont').hide()

show_polar_fields = () ->
    # show location fields for polar projection
    console.log "polar selected"
    $('#ntf-true-lat1-cont').show()
    $('#ntf-true-lat2-cont').hide()
    $('#ntf-stand-lon-cont').show()
    $('#ntf-pole-lat-cont').hide()
    $('#ntf-pole-lon-cont').hide()

show_latlon_fields = () ->
    # show location fields for mercator projection
    console.log "lat-lon selected"
    $('#ntf-true-lat1-cont').hide()
    $('#ntf-true-lat2-cont').hide()
    $('#ntf-stand-lon-cont').show()
    $('#ntf-pole-lat-cont').show()
    $('#ntf-pole-lon-cont').show()


class Domain
    constructor: (name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start) ->
        @id = NaN
        @name = name.trim()
        @width = parseInt(width)
        @height = parseInt(height)
        @dx = parseInt(dx)
        @dy = parseInt(dy)
        @ratio = parseInt(ratio)
        
        @parent_id = parseInt(parent_id)
        if isNaN(@parent_id)
            @parent_id = 0
            @i_parent_start = 0
            @j_parent_start = 0
        else
            @i_parent_start = parseInt(i_parent_start)
            @j_parent_start = parseInt(j_parent_start)
        
    
    assign_id: () ->
        # assign new id
        if isNaN(@id)
            @id = window.aqm.domain_last_id + 1
            window.aqm.domain_last_id = @id
    
    check_name: () ->
        if @name.length > 0
            return true
        else
            return false
    
    check_width: () ->
        return not isNaN(@width)
        
    check_height: () ->
        return not isNaN(@height)
        
    check_dx: () ->
        return not isNaN(@dx)
        
    check_dy: () ->
        return not isNaN(@dy)
        
    check_ratio: () ->
        return not isNaN(@ratio)
        
    check_i_parent_start: () ->
        return not isNaN(@i_parent_start)
        
    check_j_parent_start: () ->
        return not isNaN(@j_parent_start)
        
    check_parent_id: () ->
        if @parent_id == 0
            return false
        else
            return true
    
    check_all: () ->
        if @check_parent_id()
            # this is a child domain
            if @check_name() and @check_width() and @check_height() and @check_dx() and @check_dy() and @check_ratio() and @check_ratio() and @check_i_parent_start() and @check_j_parent_start()
                return true
            else
                return false
        else
            # this is not a child domain
            if @check_name() and @check_width() and @check_height() and @check_dx() and @check_dy() and @check_ratio() and @check_ratio()
                return true
            else
                return false
