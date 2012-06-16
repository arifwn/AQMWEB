
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
    
    # add domain button event handler
    $('#btn-add-domain').click((e) ->
        e.preventDefault()
        reset_domain_modal()
        show_parent_ij_field($('#ntf-parent-domain').val())
        $('#domain-modal').modal('show')
    )
    
    # remove domain button event handler
    $('#btn-remove-domain').click((e) ->
        e.preventDefault()
        remove_selected_domain()
        render_domain_list()
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
    
    # update domain table
    render_domain_list()
)


remove_selected_domain = () ->
    # remove all selected domain
    # if the domain has childs, they will be removed too
    
    # obtain a list of selected domains
    domains = get_selected_domains()
    
    # if no selected domain, just return
    if domains.length == 0
        return
    
    # confirm action to prevent accidental deletion
    if window.confirm "Remove selected domain(s) and all its subdomain?"
        # for each domain
        # remove the domain and it's child
        remove_domain(domain.id) for domain in domains

remove_domain = (domain_id) ->
    # remove a domain and all its childs
    # attempt to obtain the domain from global list
    domain = get_domain(domain_id)
    if domain?
        # if the domain exist in global domain list
        # attempt to obtain the child domain
        child_domains = get_child_domain(domain.id)
        # remove child domain recursively
        remove_domain child_domain.id for child_domain in child_domains
        # remove the domain
        remove_single_domain domain.id

remove_single_domain = (domain_id) ->
    # remove a domain from global list
    domain_id = parseInt(domain_id)
    window.aqm.domain_list = (domain for domain in window.aqm.domain_list when domain.id != domain_id)

get_child_domain = (domain_id) ->
    # obtain a list of child domain from this domain id
    domain_id = parseInt(domain_id)
    (domain for domain in window.aqm.domain_list when domain.parent_id == domain_id)

get_selected_domains = () ->
    # return a list of selected domains
    checkbox_list = $('#domain-list input[type]=checkbox:checked')
    (get_domain($(checkbox).attr('data-domain-id')) for checkbox in checkbox_list)


render_domain_list = () ->
    # render the domain table
    # remove existing rows
    $('#domain-list tr[data-domain-listing]').remove()
    
    # render all domain it the table
    render_domain domain for domain in window.aqm.domain_list
    
    # add event handler to handle editing domain
    $('a.domain_link_edit').click((e) ->
        e.preventDefault()
        id = parseInt($(e.target).attr('data-domain-id'))
        domain = get_domain(id)
        
        reset_domain_modal()
        
        # attached edited domain id
        $('#domain-modal').attr('data-domain-id', domain.id)
        
        # set modal title
        $('#domain-modal .modal-header h3').text('Edit Domain')
        
        $('#ntf-parent-domain').val(domain.parent_id)
        $('#ntf-dom-name').val(domain.name)
        $('#ntf-dom-width').val(domain.width)
        $('#ntf-dom-height').val(domain.height)
        $('#ntf-dom-dx').val(domain.dx)
        $('#ntf-dom-dy').val(domain.dy)
        $('#ntf-ratio').val(domain.ratio)
        $('#ntf-dom-parent-start-i').val(domain.i_parent_start)
        $('#ntf-dom-parent-start-j').val(domain.j_parent_start)
        
        show_parent_ij_field(domain.parent_id)
        $('#domain-modal').modal('show')
    )


render_domain = (domain) ->
    # appent a domain info into the table
    parent_domain = get_domain domain.parent_id
    parent_domain_name = '--'
    if parent_domain?
        parent_domain_name = parent_domain.name
    $('#domain-list > tbody:last').append """<tr data-domain-listing="listing"><td><input type="checkbox" data-domain-id="#{ domain.id }"></td><td><a href="#domain-#{ domain.id }" class="domain_link_edit" data-domain-id="#{ domain.id }">#{ domain.name }</a></td><td>#{ parent_domain_name }</td><td>#{ domain.width }</td><td>#{ domain.height }</td><td>#{ domain.dx }</td><td>#{ domain.dy }</td></tr>"""
    

get_domain = (domain_id) ->
    # return domain object from global list
    domain_id = parseInt(domain_id)
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
    dx = 1000
    dy = 1000
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
    
    if (domain_id < 1) or (not domain_id?)
        # add new domain
        return add_domain()
    else
        # edit existing domain
        return update_domain()

update_domain = () ->
    # update existing domain
    domain = get_domain($('#domain-modal').attr('data-domain-id'))
    
    if domain.check_all()
        domain.name = $('#ntf-dom-name').val()
        domain.width = parseInt $('#ntf-dom-width').val()
        domain.height = parseInt $('#ntf-dom-height').val()
        domain.dx = parseInt $('#ntf-dom-dx').val()
        domain.dy = parseInt $('#ntf-dom-dy').val()
        domain.ratio = parseInt $('#ntf-ratio').val()
        domain.parent_id = parseInt $('#ntf-parent-domain').val()
        domain.i_parent_start = parseInt $('#ntf-dom-parent-start-i').val()
        domain.j_parent_start = parseInt $('#ntf-dom-parent-start-j').val()
        render_domain_list()
        return true
    else
        return false

add_domain = () ->
    # add new domain
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
        render_domain_list()
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



# Coordinate Settings

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


show_location_fields = (projection) ->
    # show relevant location fields based on selected projection type
    switch projection
        when "mercator" then show_mercator_fields()
        when "lambert" then show_lambert_fields()
        when "polar" then show_polar_fields()
        when "lat-lon" then show_latlon_fields()


show_mercator_fields = () ->
    # show location fields for mercator projection
    $('#ntf-true-lat1-cont').show()
    $('#ntf-true-lat2-cont').hide()
    $('#ntf-stand-lon-cont').hide()
    $('#ntf-pole-lat-cont').hide()
    $('#ntf-pole-lon-cont').hide()

show_lambert_fields = () ->
    # show location fields for lambert conformal projection
    $('#ntf-true-lat1-cont').show()
    $('#ntf-true-lat2-cont').show()
    $('#ntf-stand-lon-cont').show()
    $('#ntf-pole-lat-cont').hide()
    $('#ntf-pole-lon-cont').hide()

show_polar_fields = () ->
    # show location fields for polar projection
    $('#ntf-true-lat1-cont').show()
    $('#ntf-true-lat2-cont').hide()
    $('#ntf-stand-lon-cont').show()
    $('#ntf-pole-lat-cont').hide()
    $('#ntf-pole-lon-cont').hide()


show_latlon_fields = () ->
    # show location fields for mercator projection
    $('#ntf-true-lat1-cont').hide()
    $('#ntf-true-lat2-cont').hide()
    $('#ntf-stand-lon-cont').show()
    $('#ntf-pole-lat-cont').show()
    $('#ntf-pole-lon-cont').show()


# Utility functions

get_float = (source, container='') ->
    # attemp to get a float from source element.
    # on success remove error class from container and vice versa
    val = parseFloat $(source).val()
    if isNaN(val)
        $(container).addClass 'error'
    else
        $(container).removeClass 'error'
    return val


# Representation of WRF domain

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
