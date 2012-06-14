
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
        save_domain($('#domain-modal').attr('data-domain-id'))
        
        $('#domain-modal').modal('hide')
    )
    
    # close domain modal window
    $('#btn-domain-modal-cancel').click((e) ->
        e.preventDefault()
        $('#domain-modal').modal('hide')
    )
    
)

save_domain = (domain_id) ->
    domain_id = parseInt(domain_id)
    
    if isNaN(domain_id)
        console.log 'add new domain'
        add_domain()
    else
        console.log 'edit existing domain'

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
    
    window.aqm.domain_list.push domain

show_parent_ij_field = (parent_domain) ->
    # if parent_domain is '-', hide parent i j position fields, and vice versa
    parent_id = parseInt(parent_domain)
    
    if isNaN(parent_id)
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
    
    # set mode to 'add'
    $('#domain-modal').attr('data-domain-id', '-')
    

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
        if isNaN(@parent)
            @i_parent_start = NaN
            @j_parent_start = NaN
        else
            @i_parent_start = parseInt(i_parent_start)
            @j_parent_start = parseInt(j_parent_start)
        
        if isNaN(@id)
            # assign new id
            @id = window.aqm.domain_last_id + 1
            window.aqm.domain_last_id = @id
    
    check_name: () ->
        if @name.length > 0
            return true
        else
            return false
    
    check_width: () ->
        return isNaN(@width)
        
    check_height: () ->
        return isNaN(@height)
        
    check_dx: () ->
        return isNaN(@dx)
        
    check_dy: () ->
        return isNaN(@dy)
        
    check_ratio: () ->
        return isNaN(@ratio)
        
    check_i_parent_start: () ->
        return isNaN(@i_parent_start)
        
    check_j_parent_start: () ->
        return isNaN(@j_parent_start)
        
    check_parent_id: () ->
        return isNaN(@parent_id)
        
