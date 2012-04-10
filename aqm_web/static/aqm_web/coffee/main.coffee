
window.aqm = {}

# display alert box
window.aqm.alert = (title, message) ->
    $('#alert-modal .modal-header h3').text title
    $('#alert-modal .modal-body p').text message
    $('#alert-modal').modal('show')
    