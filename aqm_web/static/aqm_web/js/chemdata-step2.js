(function() {
  var pollutant,
    __indexOf = Array.prototype.indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  pollutant = (function() {

    function pollutant(config) {
      var default_param, param;
      default_param = {
        id: '',
        worksheet: 0,
        conversion_factor: 1.0,
        row_start: 0,
        row_end: 0,
        emission: 'A',
        lat: 'B',
        lon: 'C',
        x: 'D',
        y: 'E'
      };
      param = $.extend(config(default_param));
      this.id = param.id;
      this.worksheet = param.worksheet;
      this.conversion_factor = param.conversion_factor;
      this.row_start = param.row_start;
      this.row_end = param.row_end;
      this.lat = param.lat;
      this.lon = param.lon;
      this.x = param.x;
      this.y = param.y;
    }

    return pollutant;

  })();

  $(document).ready(function() {
    var all_pollutant_code, all_pollutant_name, current_pollutant, display_pollutant_list, i, pollutant_list, remove_pollutant, reset_available_pollutant, sheet, worksheets, _len;
    pollutant_list = [];
    current_pollutant = [];
    all_pollutant_code = ['E_ALD', 'E_CO', 'E_CSL', 'E_ECI', 'E_ECJ', 'E_ETH', 'E_HC3', 'E_HC5', 'E_HC8', 'E_HCHO', 'E_ISO', 'E_KET', 'E_NH3', 'E_NO', 'E_NO3I', 'E_NO3J', 'E_OL2', 'E_OLI', 'E_OLT', 'E_ORA2', 'E_ORGI', 'E_ORGJ', 'E_PM25I', 'E_PM25J', 'E_PM_10', 'E_SO2', 'E_SO4I', 'E_SO4J', 'E_TOL', 'E_XYL'];
    all_pollutant_name = ['ALD', 'CO', 'CSL', 'ECI', 'ECJ', 'ETH', 'HC3', 'HC5', 'HC8', 'HCHO', 'ISO', 'KET', 'NH3', 'NO', 'NO3I', 'NO3J', 'OL2', 'OLI', 'OLT', 'ORA2', 'ORGI', 'ORGJ', 'PM25I', 'PM25J', 'PM_10', 'SO2', 'SO4I', 'SO4J', 'TOL', 'XYL'];
    remove_pollutant = function(id) {
      var new_list, plt;
      new_list = (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = pollutant_list.length; _i < _len; _i++) {
          plt = pollutant_list[_i];
          if (plt.id !== id) _results.push(plt);
        }
        return _results;
      })();
      return pollutant_list = new_list;
    };
    display_pollutant_list = function() {
      return console.log($('#chemdata-param-list'));
    };
    reset_available_pollutant = function() {
      var i, plt_id, plt_name, _len, _results;
      $('#id-pollutant-list').html('');
      _results = [];
      for (i = 0, _len = all_pollutant_code.length; i < _len; i++) {
        plt_id = all_pollutant_code[i];
        if (__indexOf.call(current_pollutant, plt_id) >= 0) continue;
        plt_name = all_pollutant_name[i];
        _results.push($('#id-pollutant-list').append("<option value=\"" + plt_id + "\">" + plt_name + "</option>"));
      }
      return _results;
    };
    $('#chemdata-add-pollutant').bind('click', function(event) {
      return $('#area-modal').modal('show');
    });
    $('#chemdata-edit-pollutant').bind('click', function(event) {
      return $('#area-modal').modal('show');
    });
    $('#chemdata-remove-pollutant').bind('click', function(event) {
      return console.log($('#chemdata-param-list'));
    });
    $('#chemdata-modal-cancel').bind('click', function(event) {
      return $('#area-modal').modal('hide');
    });
    $('#area-modal').modal({
      backdrop: true,
      keyboard: true,
      show: false
    });
    reset_available_pollutant();
    worksheets = [];
    try {
      worksheets = $.parseJSON($('#chemdata-param-list').attr('data-worksheets'));
    } catch (_error) {}
    console.log(worksheets);
    $('#id-worksheet-list').html('');
    for (i = 0, _len = worksheets.length; i < _len; i++) {
      sheet = worksheets[i];
      $('#id-worksheet-list').append("<option value=\"" + i + "\">" + sheet + "</option>");
    }
    return display_pollutant_list();
  });

}).call(this);
