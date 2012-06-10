
window.aqm.chemdata = {}

# list of pollutant object
window.aqm.chemdata.pollutant_list = []

# list of pollutant id
window.aqm.chemdata.pollutant_id_list = []


class Pollutant
    constructor: (config) ->
        default_param = 
            pollutant: ''
            worksheet: 0
            conversion_factor: 1.0
            row_start: 0
            row_end: 0
            data_w: 0
            data_h: 0
            value: 'A'
            lat: 'B'
            lon: 'C'
            x: 'D'
            y: 'E'
            hourly_fluctuation: '[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]'
        
        param = $.extend default_param, config
        
        @pollutant = param.pollutant.trim()
        @worksheet = parseInt param.worksheet
        @conversion_factor = parseFloat param.conversion_factor
        @row_start = parseInt param.row_start
        @row_end = parseInt param.row_end
        @data_w = parseInt param.data_w
        @data_h = parseInt param.data_h
        @value = param.value.trim().toUpperCase()
        @lat = param.lat.trim().toUpperCase()
        @lon = param.lon.trim().toUpperCase()
        @x = param.x.trim().toUpperCase()
        @y = param.y.trim().toUpperCase()
        @hourly_fluctuation = param.hourly_fluctuation.trim()
    
    validate: () ->
        if @pollutant.length == 0
            return false
        if isNaN @worksheet
            return false
        if isNaN @conversion_factor
            return false
        if isNaN @row_start
            return false
        if isNaN @row_end
            return false
        if isNaN @data_w
            return false
        if isNaN @data_h
            return false
        if @value.length == 0
            return false
        if @lat.length == 0
            return false
        if @lon.length == 0
            return false
        if @x.length == 0
            return false
        if @y.length == 0
            return false
        
        try
            hourly_factors = JSON.parse(@hourly_fluctuation)
        catch SyntaxError
            
        if hourly_factors.length != 24
            return false
        
        return true
        

all_pollutant_code = [
    'E_ALD', 'E_CO', 'E_CSL', 'E_ECI', 'E_ECJ', 
    'E_ETH', 'E_HC3', 'E_HC5', 'E_HC8', 'E_HCHO', 
    'E_ISO', 'E_KET', 'E_NH3', 'E_NO', 'E_NO3I', 
    'E_NO3J', 'E_OL2', 'E_OLI', 'E_OLT', 'E_ORA2', 
    'E_ORGI', 'E_ORGJ', 'E_PM25I', 'E_PM25J', 'E_PM_10', 
    'E_SO2', 'E_SO4I', 'E_SO4J', 'E_TOL', 'E_XYL'
]

all_pollutant_name = [
    'ALD', 'CO', 'CSL', 'ECI', 'ECJ', 
    'ETH', 'HC3', 'HC5', 'HC8', 'HCHO', 
    'ISO', 'KET', 'NH3', 'NO', 'NO3I', 
    'NO3J', 'OL2', 'OLI', 'OLT', 'ORA2', 
    'ORGI', 'ORGJ', 'PM25I', 'PM25J', 'PM_10', 
    'SO2', 'SO4I', 'SO4J', 'TOL', 'XYL'
]


# process retrieved chemdata
window.process_chemdata = (data) ->
    window.aqm.chemdata.chemdata = data
    window.aqm.chemdata.pollutant_list = []
    window.aqm.chemdata.pollutant_list.push pollutant for pollutant in data.parameters
    window.aqm.chemdata.pollutant_id_list = []
    window.aqm.chemdata.pollutant_id_list.push pollutant.pollutant for pollutant in data.parameters
    
    # reset pollutant widget in modal dialog
    update_pollutant_list_modal()
    reset_pollutant_listbox()

# remove listed pollutants
remove_pollutants = (pollutant_list) ->
    window.aqm.chemdata.pollutant_list = (plt for plt in window.aqm.chemdata.pollutant_list when plt.pollutant not in pollutant_list)

# return pollutant data from pollutant id
get_pollutant_data = (pollutant_id) ->
    index = window.aqm.chemdata.pollutant_id_list.indexOf pollutant_id
    return window.aqm.chemdata.pollutant_list[index]
    
# return pollutant name from pollutant id
get_pollutant_name = (pollutant_id) ->
    index = all_pollutant_code.indexOf pollutant_id
    return all_pollutant_name[index]

# return pollutant id from pollutant name
get_pollutant_id = (pollutant_name) ->
    index = all_pollutant_name.indexOf pollutant_name
    return all_pollutant_code[index]
    

# remove pollutant from list by rebuilding the list and skip removed pollutant
remove_pollutant = (pollutant) ->
    window.aqm.chemdata.pollutant_list = (plt for plt in window.aqm.chemdata.pollutant_list when plt.pollutant != pollutant)
    window.aqm.chemdata.pollutant_id_list = (plt.pollutant for plt in window.aqm.chemdata.pollutant_list)

# reset select widget to only display pollutants that haven't been added yet
update_pollutant_list_modal = () ->
    $('#id-pollutant-list').empty()
    for pollutant, i in all_pollutant_code
        if pollutant in window.aqm.chemdata.pollutant_id_list
            continue
        pollutant_name = all_pollutant_name[i]
        $('#id-pollutant-list').append "<option value=\"#{ pollutant }\">#{ pollutant_name }</option>"

# reset select widget to display all pollutants type
reset_pollutant_list_modal = () ->
    $('#id-pollutant-list').empty()
    for pollutant, i in all_pollutant_code
        pollutant_name = all_pollutant_name[i]
        $('#id-pollutant-list').append "<option value=\"#{ pollutant }\">#{ pollutant_name }</option>"

# set select widget to only display specified pollutants type
set_pollutant_list_modal = (pollutant_id) ->
    $('#id-pollutant-list').empty()
    pollutant_name = get_pollutant_name pollutant_id
    $('#id-pollutant-list').append "<option value=\"#{ pollutant_id }\">#{ pollutant_name }</option>"


# reset parameter list box
reset_pollutant_listbox = () ->
    $('#chemdata-param-list').empty()
    for pollutant in window.aqm.chemdata.pollutant_list
        pollutant_name = get_pollutant_name pollutant.pollutant
        $('#chemdata-param-list').append "<option value=\"#{ pollutant.pollutant }\">#{ pollutant_name }</option>"

# edit pollutant in modal dialog
edit_pollutant = (pollutant_id) ->
    pollutant = get_pollutant_data pollutant_id
    
    # reset pollutant widget in modal dialog
    set_pollutant_list_modal pollutant_id
    
    # populate dialog field with current data
    $('#id-pollutant-list').val(pollutant.pollutant)
    $('#id-worksheet-list').val(pollutant.worksheet)
    $('#id-conv-factor').val(pollutant.conversion_factor)
    $('#id-data-row-start').val(pollutant.row_start)
    $('#id-data-row-end').val(pollutant.row_end)
    $('#id-data-dim-w').val(pollutant.data_w)
    $('#id-data-dim-h').val(pollutant.data_h)
    $('#id-emission-col').val(pollutant.value)
    $('#id-lat-col').val(pollutant.lat)
    $('#id-lon-col').val(pollutant.lon)
    $('#id-x-col').val(pollutant.x)
    $('#id-y-col').val(pollutant.y)
    $('#id-hourly-fluctuation').val(pollutant.hourly_fluctuation)
    
    # metadata for save command; 'save' will need to know whether this is edit or add
    $('#area-modal').attr 'data-command', 'edit'
    $('#area-modal').attr 'data-command-param', pollutant.pollutant
    
    $('#area-modal').modal 'show'

# show add pollutant modal dialog
add_pollutant = () ->
    # reset select widget to only display pollutants that haven't been added yet
    update_pollutant_list_modal()
    
    # reset dialog field
    $('#id-pollutant-list').val("")
    $('#id-worksheet-list').val("")
    $('#id-conv-factor').val("")
    $('#id-data-row-start').val("")
    $('#id-data-row-end').val("")
    $('#id-data-dim-w').val("")
    $('#id-data-dim-h').val("")
    $('#id-emission-col').val("")
    $('#id-lat-col').val("")
    $('#id-lon-col').val("")
    $('#id-x-col').val("")
    $('#id-y-col').val("")
    $('#id-hourly-fluctuation').val("")
    
    # metadata for save command; 'save' will need to know whether this is edit or add
    $('#area-modal').attr 'data-command', 'add'
    $('#area-modal').attr 'data-command-param', ''
    
    $('#area-modal').modal 'show'

# save editted pollutant data
save_pollutant = () ->
    command = $('#area-modal').attr 'data-command'
    target_pollutant = $('#area-modal').attr 'data-command-param'
    
    param =
        pollutant : $('#id-pollutant-list').val()
        worksheet : $('#id-worksheet-list').val()
        conversion_factor : $('#id-conv-factor').val()
        row_start : $('#id-data-row-start').val()
        row_end : $('#id-data-row-end').val()
        data_w : $('#id-data-dim-w').val()
        data_h : $('#id-data-dim-h').val()
        value : $('#id-emission-col').val()
        lat : $('#id-lat-col').val()
        lon : $('#id-lon-col').val()
        x : $('#id-x-col').val()
        y : $('#id-y-col').val()
        hourly_fluctuation: $('#id-hourly-fluctuation').val()
    
    plt = new Pollutant param
    
    switch command
        when "add"
            if plt.validate()
                window.aqm.chemdata.pollutant_list.push plt
                window.aqm.chemdata.pollutant_id_list.push plt.pollutant
                reset_pollutant_listbox()
                return true
            else
                return false
        
        when "edit"
            original_data = get_pollutant_data target_pollutant
            
            if plt.validate()
                original_data.worksheet = plt.worksheet
                original_data.conversion_factor = plt.conversion_factor
                original_data.row_start = plt.row_start
                original_data.row_end = plt.row_end
                original_data.data_w = plt.data_w
                original_data.data_h = plt.data_h
                original_data.value = plt.value
                original_data.lat = plt.lat
                original_data.lon = plt.lon
                original_data.x = plt.x
                original_data.y = plt.y
                original_data.hourly_fluctuation = plt.hourly_fluctuation
                reset_pollutant_listbox()
                return true
            else
                return false

$(document).ready(->
    
    $('#chemdata-add-pollutant').bind 'click', (event) ->
        # add new pollutant
        add_pollutant()
    
    $('#chemdata-edit-pollutant').bind 'click', (event) ->
        # edit selected polutant
        edit_list = $('#chemdata-param-list').val()
        if edit_list != null
            if edit_list.length > 0
                edit_pollutant edit_list[0]
    
    $('#chemdata-remove-pollutant').bind 'click', (event) ->
        # remove selected pollutant
        removal_list = $('#chemdata-param-list').val()
        remove_pollutants removal_list
        reset_pollutant_listbox()
        # console.log removal_list
    
    $('#chemdata-modal-cancel').bind 'click', (event) ->
        # close modal
        $('#area-modal').modal 'hide'
    
    $('#chemdata-modal-ok').bind 'click', (event) ->
        # save pollutant data
        if save_pollutant()
            $('#area-modal').modal 'hide'
        else
            window.aqm.alert "Error", "Check your input!"
    
    $('#chemdata-save').bind 'click', (event) ->
        $(event.target).button('loading')
        
        # console.log JSON.stringify window.aqm.chemdata.pollutant_list
        
        chemdata_id = window.aqm.chemdata.chemdata.id
        parameters_json = JSON.stringify window.aqm.chemdata.pollutant_list
        
        $.ajax {url: chemdata_url,
        dataType: 'json',
        type: 'POST',
        data: {chemdata_id: chemdata_id, parameters_json: parameters_json, display_message: true},
        success: (data) ->
            $(event.target).button('reset')
            # console.log data
            if data
                window.location.replace window.chemdata_list_url
        ,
        error: (jqXHR, textStatus, errorThrown) ->
            $(event.target).button('reset')
            if jqXHR.status == 0
                window.aqm.alert("Connectivity Error", "Cannot connect to remote server: " + textStatus + " " + errorThrown);
            else if jqXHR.status == 400
                window.aqm.alert("Error", "Invalid data received. Please check your input.");
            else if jqXHR.status == 404
                window.aqm.alert("Error", "Resource Not Found");
            else if jqXHR.status == 500
                window.aqm.alert("Error", "Internal Server Error");
            else if jqXHR.status == 503
                window.aqm.alert("Error", "Server temporarily unavailable!");
            
        }
    
    $('#chemdata-conversion-factor-evaluate').bind 'click', (event) ->
        # evaluate conversion factor arithmatic
        event.preventDefault()
        $('#id-conv-factor').val(eval($('#id-conv-factor').val()))
    
    $('#chemdata-default-hourly-fluctuation').bind 'click', (event) ->
        # fill default value
        event.preventDefault()
        $('#id-hourly-fluctuation').val('[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]')
        
    # -- Entry Point --
    
    # initialize modal
    $('#area-modal').modal({backdrop: true, keyboard: true, show: false});
    
    # initialize worksheet list
    worksheets = []
    try
        worksheets = $.parseJSON $('#chemdata-param-list').attr('data-worksheets')
    
    $('#id-worksheet-list').html ''
    for sheet, i in worksheets
        $('#id-worksheet-list').append("<option value=\"#{i}\">#{sheet}</option>")
    
    
)