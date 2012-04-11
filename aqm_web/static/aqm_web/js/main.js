
  window.aqm = {};

  window.aqm.alert = function(title, message) {
    $('#alert-modal .modal-header h3').text(title);
    $('#alert-modal .modal-body p').text(message);
    return $('#alert-modal').modal('show');
  };
