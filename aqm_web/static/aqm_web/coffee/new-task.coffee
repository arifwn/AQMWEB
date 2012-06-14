
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
    
    # add domain button
    $('#btn-add-domain').click((e) ->
        e.preventDefault()
        reset_domain_modal()
        $('#domain-modal').modal('show')
    )
    
    # close domain modal window
    $('#btn-domain-modal-cancel').click((e) ->
        e.preventDefault()
        $('#domain-modal').modal('hide')
    )
    
    # domain modal window save button
    $('#btn-domain-modal-ok').click((e) ->
        e.preventDefault()
        
        # add or edit the domain
        
        $('#domain-modal').modal('hide')
    )
    
)

reset_domain_modal = () ->
    # reset fields on domain modal window
    title = 'Add New Domain'
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
