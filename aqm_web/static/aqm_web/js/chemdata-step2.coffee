class pollutant
  constructor: (config) ->
    default_param = 
      id: ''
      worksheet: 0
      conversion_factor: 1.0
      row_start: 0
      row_end: 0
      emission: 'A'
      lat: 'B'
      lon: 'C'
      x: 'D'
      y: 'E'
    
    param = $.extend config default_param
    
    @id = param.id
    @worksheet = param.worksheet
    @conversion_factor = param.conversion_factor
    @row_start = param.row_start
    @row_end = param.row_end
    @lat = param.lat
    @lon = param.lon
    @x = param.x
    @y = param.y

$(document).ready(->
  pollutant_list = []
  
  current_pollutant = []
  
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
  
  remove_pollutant = (id) ->
    # remove pollutant from list by rebuilding the list and skip removed pollutant
    new_list = (plt for plt in pollutant_list when plt.id != id)
    pollutant_list = new_list
  
  display_pollutant_list = ->
    console.log($('#chemdata-param-list'))
  
  reset_available_pollutant = () ->
    # reset select widget to only display pollutants that haven't added yet
    $('#id-pollutant-list').html ''
    for plt_id, i in all_pollutant_code
      if plt_id in current_pollutant
        continue
      plt_name = all_pollutant_name[i]
      $('#id-pollutant-list').append "<option value=\"#{plt_id}\">#{plt_name}</option>"
      
  
  $('#chemdata-add-pollutant').bind 'click', (event) ->
    # add new pollutant
    $('#area-modal').modal 'show'
  
  $('#chemdata-edit-pollutant').bind 'click', (event) ->
    # edit selected polutant
   $('#area-modal').modal 'show'
  
  $('#chemdata-remove-pollutant').bind 'click', (event) ->
    # remove selected pollutant
    console.log($('#chemdata-param-list'))
  
  $('#chemdata-modal-cancel').bind 'click', (event) ->
    # close modal
    $('#area-modal').modal 'hide'
  
  
  # -- Entry Point --
  
  # initialize modal
  $('#area-modal').modal({backdrop: true, keyboard: true, show: false});
  
  reset_available_pollutant()
  
  # initialize worksheet list
  worksheets = []
  try
    worksheets = $.parseJSON $('#chemdata-param-list').attr('data-worksheets')
  
  console.log worksheets
  $('#id-worksheet-list').html ''
  for sheet, i in worksheets
    $('#id-worksheet-list').append("<option value=\"#{i}\">#{sheet}</option>")
  
  # display pollutants in list box
  display_pollutant_list()
  
)