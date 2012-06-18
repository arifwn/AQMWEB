// Generated by CoffeeScript 1.3.1
(function() {
  var Domain, add_domain, append_parent_dropdown_list, get_all_user_chem, get_child_domain, get_current_user_chem, get_domain, get_float, get_selected_domains, init_date_picker, init_test_data, remove_domain, remove_selected_domain, remove_single_domain, render_chemdata_list, render_domain_list, reset_chem_modal, reset_domain_modal, save_domain, set_emission_data, show_chem_modal, show_lambert_fields, show_latlon_fields, show_location_fields, show_map_modal, show_mercator_fields, show_parent_ij_field, show_polar_fields, show_preview_map, submit_data, update_domain;

  $(document).ready(function() {
    $('#ntf-proj').change(function(e) {
      var proj;
      e.preventDefault();
      proj = $('#ntf-proj').val();
      return show_location_fields(proj);
    });
    show_location_fields($('#ntf-proj').val());
    $('#btn-map-preview').click(function(e) {
      var latitude, longitude, true_lat;
      e.preventDefault();
      latitude = get_float('#ntf-ref-lat', '#ntf-ref-container');
      longitude = get_float('#ntf-ref-lon', '#ntf-ref-container');
      if (isNaN(latitude) || isNaN(longitude)) {

      } else {
        true_lat = Math.abs(latitude);
        if (isNaN(get_float('#ntf-true-lat1'))) {
          $('#ntf-true-lat1').val(true_lat);
        }
        return show_preview_map(latitude, longitude);
      }
    });
    $('#btn-area-modal-close').click(function(e) {
      e.preventDefault();
      return $('#area-modal').modal('hide');
    });
    $('#area-modal').on('hidden', function() {
      return spinner_func.spinner_stop('#map-loading-spinner');
    });
    window.aqm.domain_list = [];
    window.aqm.domain_last_id = 0;
    $('#btn-add-domain').click(function(e) {
      e.preventDefault();
      reset_domain_modal();
      show_parent_ij_field($('#ntf-parent-domain').val());
      return $('#domain-modal').modal('show');
    });
    $('#btn-remove-domain').click(function(e) {
      e.preventDefault();
      remove_selected_domain();
      return render_domain_list();
    });
    $('#ntf-parent-domain').change(function(e) {
      e.preventDefault();
      return show_parent_ij_field($('#ntf-parent-domain').val());
    });
    $('#btn-domain-modal-ok').click(function(e) {
      e.preventDefault();
      if (save_domain($('#domain-modal').attr('data-domain-id'))) {
        return $('#domain-modal').modal('hide');
      } else {
        return window.aqm.alert("Error!", "Please check your input!");
      }
    });
    $('#btn-domain-modal-cancel').click(function(e) {
      e.preventDefault();
      return $('#domain-modal').modal('hide');
    });
    init_test_data();
    render_domain_list();
    window.aqm.chemdata_id = 0;
    $('#ntf-chem-select-data').click(function(e) {
      e.preventDefault();
      reset_chem_modal();
      return show_chem_modal();
    });
    $('#btn-chem-modal-cancel').click(function(e) {
      e.preventDefault();
      return $('#chem-modal').modal('hide');
    });
    $('#btn-chem-modal-ok').click(function(e) {
      e.preventDefault();
      if (set_emission_data()) {
        return $('#chem-modal').modal('hide');
      } else {
        return window.aqm.alert("Error!", "Please check your input!");
      }
    });
    init_date_picker();
    return $('#wrf-new-task-form').submit(function(e) {
      submit_data();
      return false;
    });
  });

  submit_data = function() {
    var data;
    data = {
      name: $('#task-name').val(),
      description: tinymce.get('task-description').getContent(),
      start_time: "",
      end_time: "",
      ref_lat: 0,
      ref_lon: 0,
      projection: "",
      true_scale_lat: 0,
      true_scale_lat2: 0,
      stand_lon: 0,
      pole_lat: 0,
      pole_lon: 0,
      domains: [],
      use_chem: false,
      chem_data_list: []
    };
    return console.log(data);
  };

  init_date_picker = function() {
    $('#ntf-start-date').datepicker({
      dateFormat: 'dd-mm-yy'
    });
    $('#ntf-start-time').timepicker({
      defaultTime: '00:00',
      onHourShow: function(hour) {
        if ((hour === 0) || (hour === 6) || (hour === 12) || (hour === 18)) {
          return true;
        } else {
          return false;
        }
      },
      onMinuteShow: function(hour, minute) {
        if (minute === 0) {
          return true;
        } else {
          return false;
        }
      }
    });
    $('#ntf-end-date').datepicker({
      dateFormat: 'dd-mm-yy'
    });
    return $('#ntf-end-time').timepicker({
      defaultTime: '12:00',
      onHourShow: function(hour) {
        if ((hour === 0) || (hour === 6) || (hour === 12) || (hour === 18)) {
          return true;
        } else {
          return false;
        }
      },
      onMinuteShow: function(hour, minute) {
        if (minute === 0) {
          return true;
        } else {
          return false;
        }
      }
    });
  };

  get_all_user_chem = function() {
    return $.ajax({
      url: aqm.chem_list_all_url,
      dataType: 'json',
      type: 'GET',
      success: function(data) {
        $('#chem-modal .modal-body').empty();
        return render_chemdata_list(data, true);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        $('#chem-modal .modal-body').empty();
        return $('#chem-modal .modal-body').append("<div class=\"alert alert-error\"><p>" + textStatus + "</p><p>" + errorThrown + "</p></div>");
      }
    });
  };

  get_current_user_chem = function() {
    return $.ajax({
      url: aqm.chem_list_url,
      dataType: 'json',
      type: 'GET',
      success: function(data) {
        $('#chem-modal .modal-body').empty();
        return render_chemdata_list(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        $('#chem-modal .modal-body').empty();
        return $('#chem-modal .modal-body').append("<div class=\"alert alert-error\"><p>" + textStatus + "</p><p>" + errorThrown + "</p></div>");
      }
    });
  };

  show_chem_modal = function() {
    $.ajax({
      url: aqm.chem_list_url,
      dataType: 'json',
      type: 'GET',
      success: function(data) {
        $('#chem-modal .modal-body').empty();
        return render_chemdata_list(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        $('#chem-modal .modal-body').empty();
        return $('#chem-modal .modal-body').append("<div class=\"alert alert-error\"><p>" + textStatus + "</p><p>" + errorThrown + "</p></div>");
      }
    });
    return $('#chem-modal').modal('show');
  };

  render_chemdata_list = function(data, all_chem) {
    var button_html, checked, chemdata, param, parameter_list_str, row_html, table_html, _i, _j, _len, _len1, _ref, _results;
    if (all_chem == null) {
      all_chem = false;
    }
    button_html = "<p><input type=\"button\" id=\"btn-chem-show-all\" class=\"btn btn-info\" value=\"Show Emission Data from All User\" ></p>";
    if (all_chem) {
      button_html = "<p><input type=\"button\" id=\"btn-chem-show-my\" class=\"btn\" value=\"Show My Emission Data Only\" ></p>";
    }
    table_html = "" + button_html + "\n<table id=\"chemdata-list\" class=\"table table-striped table-bordered table-condensed\">\n    <tbody>\n        <tr>\n            <th></th>\n            <th>Name</th>\n            <th>User</th>\n            <th>Parameters</th>\n            <th>Date</th>\n        </tr>\n    </tbody>\n</table>";
    $('#chem-modal .modal-body').html(table_html);
    _results = [];
    for (_i = 0, _len = data.length; _i < _len; _i++) {
      chemdata = data[_i];
      parameter_list_str = '';
      _ref = chemdata.parameters;
      for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
        param = _ref[_j];
        parameter_list_str = "" + parameter_list_str + " " + param.pollutant;
      }
      checked = '';
      if (window.aqm.chemdata_id === chemdata.id) {
        checked = 'checked';
      }
      row_html = "<tr>\n    <td><input type=\"radio\" name=\"chemdata-radio\" data-chemdata-id=\"" + chemdata.id + "\" data-chemdata-name=\"" + chemdata.name + "\" data-user-avatar=\"/accounts/avatar/t32x32/" + chemdata.user.username + "\" data-user-name=\"" + chemdata.user.get_full_name + "\" " + checked + "></td>\n    <td>" + chemdata.name + "</td>\n    <td><img class=\"avatar-picture\" src=\"/accounts/avatar/t32x32/" + chemdata.user.username + "\" width=\"32\" height=\"32\" style=\"height: 32px;\" title=\"" + chemdata.user.get_full_name + "\" /></td>\n    <td>" + parameter_list_str + "</td>\n    <td><b>Created:</b> " + chemdata.created + " <br><b>Modified:</b> " + chemdata.modified + "</td>\n</tr>";
      $('#chemdata-list > tbody:last').append(row_html);
      $('#btn-chem-show-all').click(function(e) {
        e.preventDefault();
        reset_chem_modal();
        return get_all_user_chem();
      });
      _results.push($('#btn-chem-show-my').click(function(e) {
        e.preventDefault();
        reset_chem_modal();
        return get_current_user_chem();
      }));
    }
    return _results;
  };

  reset_chem_modal = function() {
    return $('#chem-modal .modal-body').html("<p class=\"center\"><img src=\"" + aqm.spinner_image_url + "\" alt=\"Loading...\"></p>");
  };

  set_emission_data = function() {
    var avatar_url, chemdata_id, chemdata_name, user;
    chemdata_id = parseInt($('[name=chemdata-radio]:radio:checked').attr('data-chemdata-id'));
    if ((chemdata_id < 1) || (isNaN(chemdata_id))) {
      return false;
    } else {
      window.aqm.chemdata_id = chemdata_id;
      chemdata_name = $('[name=chemdata-radio]:radio:checked').attr('data-chemdata-name');
      avatar_url = $('[name=chemdata-radio]:radio:checked').attr('data-user-avatar');
      user = $('[name=chemdata-radio]:radio:checked').attr('data-user-name');
      $('#ntf-chem-data').html("<img class=\"avatar-picture\" src=\"" + avatar_url + "\" width=\"32\" height=\"32\" style=\"height: 32px;\" title=\"" + user + "\" /> <b>" + chemdata_name + "</b>");
      return true;
    }
  };

  remove_selected_domain = function() {
    var domain, domains, _i, _len, _results;
    domains = get_selected_domains();
    if (domains.length === 0) {
      return;
    }
    if (window.confirm("Remove selected domain(s) and all its subdomain?")) {
      _results = [];
      for (_i = 0, _len = domains.length; _i < _len; _i++) {
        domain = domains[_i];
        _results.push(remove_domain(domain.id));
      }
      return _results;
    }
  };

  remove_domain = function(domain_id) {
    var child_domain, child_domains, domain, _i, _len;
    domain = get_domain(domain_id);
    if (domain != null) {
      child_domains = get_child_domain(domain.id);
      for (_i = 0, _len = child_domains.length; _i < _len; _i++) {
        child_domain = child_domains[_i];
        remove_domain(child_domain.id);
      }
      return remove_single_domain(domain.id);
    }
  };

  remove_single_domain = function(domain_id) {
    var domain;
    domain_id = parseInt(domain_id);
    return window.aqm.domain_list = (function() {
      var _i, _len, _ref, _results;
      _ref = window.aqm.domain_list;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        domain = _ref[_i];
        if (domain.id !== domain_id) {
          _results.push(domain);
        }
      }
      return _results;
    })();
  };

  get_child_domain = function(domain_id) {
    var domain, _i, _len, _ref, _results;
    domain_id = parseInt(domain_id);
    _ref = window.aqm.domain_list;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      domain = _ref[_i];
      if (domain.parent_id === domain_id) {
        _results.push(domain);
      }
    }
    return _results;
  };

  get_selected_domains = function() {
    var checkbox, checkbox_list, _i, _len, _results;
    checkbox_list = $('#domain-list input[type]=checkbox:checked');
    _results = [];
    for (_i = 0, _len = checkbox_list.length; _i < _len; _i++) {
      checkbox = checkbox_list[_i];
      _results.push(get_domain($(checkbox).attr('data-domain-id')));
    }
    return _results;
  };

  render_domain_list = function() {
    var domain, parent_domain, parent_domain_name, _i, _len, _ref;
    $('#domain-list tr[data-domain-listing]').remove();
    _ref = window.aqm.domain_list;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      domain = _ref[_i];
      parent_domain = get_domain(domain.parent_id);
      parent_domain_name = '--';
      if (parent_domain != null) {
        parent_domain_name = parent_domain.name;
      }
      $('#domain-list > tbody:last').append("<tr data-domain-listing=\"listing\"><td><input type=\"checkbox\" data-domain-id=\"" + domain.id + "\"></td><td><a href=\"#domain-" + domain.id + "\" class=\"domain_link_edit\" data-domain-id=\"" + domain.id + "\">" + domain.name + "</a></td><td>" + parent_domain_name + "</td><td>" + domain.width + "</td><td>" + domain.height + "</td><td>" + domain.dx + "</td><td>" + domain.dy + "</td></tr>");
    }
    return $('a.domain_link_edit').click(function(e) {
      var id;
      e.preventDefault();
      id = parseInt($(e.target).attr('data-domain-id'));
      domain = get_domain(id);
      reset_domain_modal();
      $('#domain-modal').attr('data-domain-id', domain.id);
      $('#domain-modal .modal-header h3').text('Edit Domain');
      $('#ntf-parent-domain').val(domain.parent_id);
      $('#ntf-dom-name').val(domain.name);
      $('#ntf-dom-width').val(domain.width);
      $('#ntf-dom-height').val(domain.height);
      $('#ntf-dom-dx').val(domain.dx);
      $('#ntf-dom-dy').val(domain.dy);
      $('#ntf-ratio').val(domain.ratio);
      $('#ntf-dom-parent-start-i').val(domain.i_parent_start);
      $('#ntf-dom-parent-start-j').val(domain.j_parent_start);
      show_parent_ij_field(domain.parent_id);
      return $('#domain-modal').modal('show');
    });
  };

  get_domain = function(domain_id) {
    var domain, _i, _len, _ref;
    domain_id = parseInt(domain_id);
    _ref = window.aqm.domain_list;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      domain = _ref[_i];
      if (domain.id === domain_id) {
        return domain;
      }
    }
  };

  init_test_data = function() {
    var domain1, domain2, domain3, dx, dy, height, i_parent_start, j_parent_start, name, parent_id, ratio, width;
    width = 50;
    height = 50;
    dx = 9000;
    dy = 9000;
    ratio = 1;
    parent_id = 0;
    i_parent_start = 0;
    j_parent_start = 0;
    name = 'Test Domain 1';
    domain1 = new Domain(name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start);
    domain1.assign_id();
    name = 'Test Domain 2';
    dx = 3000;
    dy = 3000;
    ratio = 3;
    parent_id = domain1.id;
    i_parent_start = 25;
    j_parent_start = 25;
    domain2 = new Domain(name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start);
    domain2.assign_id();
    name = 'Test Domain 3';
    dx = 1000;
    dy = 1000;
    ratio = 3;
    parent_id = domain2.id;
    i_parent_start = 25;
    j_parent_start = 25;
    domain3 = new Domain(name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start);
    domain3.assign_id();
    window.aqm.domain_list.push(domain1);
    window.aqm.domain_list.push(domain2);
    return window.aqm.domain_list.push(domain3);
  };

  save_domain = function(domain_id) {
    domain_id = parseInt(domain_id);
    if ((domain_id < 1) || (isNaN(domain_id))) {
      return add_domain();
    } else {
      return update_domain();
    }
  };

  update_domain = function() {
    var domain;
    domain = get_domain($('#domain-modal').attr('data-domain-id'));
    if (domain.check_all()) {
      domain.name = $('#ntf-dom-name').val();
      domain.width = parseInt($('#ntf-dom-width').val());
      domain.height = parseInt($('#ntf-dom-height').val());
      domain.dx = parseInt($('#ntf-dom-dx').val());
      domain.dy = parseInt($('#ntf-dom-dy').val());
      domain.ratio = parseInt($('#ntf-ratio').val());
      domain.parent_id = parseInt($('#ntf-parent-domain').val());
      domain.i_parent_start = parseInt($('#ntf-dom-parent-start-i').val());
      domain.j_parent_start = parseInt($('#ntf-dom-parent-start-j').val());
      render_domain_list();
      return true;
    } else {
      return false;
    }
  };

  add_domain = function() {
    var domain, dx, dy, height, i_parent_start, j_parent_start, name, parent_id, ratio, width;
    name = $('#ntf-dom-name').val();
    width = $('#ntf-dom-width').val();
    height = $('#ntf-dom-height').val();
    dx = $('#ntf-dom-dx').val();
    dy = $('#ntf-dom-dy').val();
    ratio = $('#ntf-ratio').val();
    parent_id = $('#ntf-parent-domain').val();
    i_parent_start = $('#ntf-dom-parent-start-i').val();
    j_parent_start = $('#ntf-dom-parent-start-j').val();
    domain = new Domain(name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start);
    if (domain.check_all()) {
      domain.assign_id();
      window.aqm.domain_list.push(domain);
      render_domain_list();
      return true;
    } else {
      return false;
    }
  };

  show_parent_ij_field = function(parent_domain) {
    var parent_id;
    parent_id = parseInt(parent_domain);
    if (parent_id === 0) {
      return $('#ntf-dom-parent-start-container').hide();
    } else {
      return $('#ntf-dom-parent-start-container').show();
    }
  };

  reset_domain_modal = function() {
    var domain, title, _i, _len, _ref;
    title = 'Add New Domain';
    $('#ntf-parent-domain').val(0);
    $('#domain-modal .clearfix').removeClass('error');
    $('#domain-modal .input-prepend').removeClass('error');
    $('#domain-modal .modal-header h3').text(title);
    $('#ntf-dom-name').val('');
    $('#ntf-dom-width').val('');
    $('#ntf-dom-height').val('');
    $('#ntf-dom-dx').val('');
    $('#ntf-dom-dy').val('');
    $('#ntf-ratio').val('');
    $('#ntf-dom-parent-start-i').val('');
    $('#ntf-dom-parent-start-j').val('');
    $('#ntf-parent-domain').html('');
    $('#ntf-parent-domain').append('<option selected value="0">-- None --</option>');
    _ref = window.aqm.domain_list;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      domain = _ref[_i];
      append_parent_dropdown_list(domain);
    }
    return $('#domain-modal').attr('data-domain-id', '0');
  };

  append_parent_dropdown_list = function(domain) {
    return $('#ntf-parent-domain').append("<option value=\"" + domain.id + "\">" + domain.name + "</option>");
  };

  show_preview_map = function(latitude, longitude) {
    var lower_lat, lower_lon, map_url, true_lat, upper_lat, upper_lon;
    true_lat = Math.abs(latitude);
    upper_lat = latitude + 20;
    upper_lon = longitude + 27;
    lower_lat = latitude - 20;
    lower_lon = longitude - 27;
    if (upper_lat > 80) {
      upper_lat = 80;
      lower_lat = 80 - 40;
    }
    if (lower_lat < -80) {
      lower_lat = -80;
      upper_lat = -80 + 40;
    }
    map_url = "" + window.aqm.map_mercator_base_url + "?upper_lat=" + upper_lat + "&upper_lon=" + upper_lon + "&lower_lat=" + lower_lat + "&lower_lon=" + lower_lon + "&true_lat=" + true_lat + "&ref_lat=" + latitude + "&ref_lon=" + longitude;
    return show_map_modal(map_url);
  };

  show_map_modal = function(map_url) {
    spinner_func.spinner_play('#map-loading-spinner');
    $('#area-modal .preview-image').hide().load(function() {
      return $(this).fadeIn();
    }).attr('src', map_url);
    return $('#area-modal').modal('show');
  };

  show_location_fields = function(projection) {
    switch (projection) {
      case "mercator":
        return show_mercator_fields();
      case "lambert":
        return show_lambert_fields();
      case "polar":
        return show_polar_fields();
      case "lat-lon":
        return show_latlon_fields();
    }
  };

  show_mercator_fields = function() {
    $('#ntf-true-lat1-cont').show();
    $('#ntf-true-lat2-cont').hide();
    $('#ntf-stand-lon-cont').hide();
    $('#ntf-pole-lat-cont').hide();
    return $('#ntf-pole-lon-cont').hide();
  };

  show_lambert_fields = function() {
    $('#ntf-true-lat1-cont').show();
    $('#ntf-true-lat2-cont').show();
    $('#ntf-stand-lon-cont').show();
    $('#ntf-pole-lat-cont').hide();
    return $('#ntf-pole-lon-cont').hide();
  };

  show_polar_fields = function() {
    $('#ntf-true-lat1-cont').show();
    $('#ntf-true-lat2-cont').hide();
    $('#ntf-stand-lon-cont').show();
    $('#ntf-pole-lat-cont').hide();
    return $('#ntf-pole-lon-cont').hide();
  };

  show_latlon_fields = function() {
    $('#ntf-true-lat1-cont').hide();
    $('#ntf-true-lat2-cont').hide();
    $('#ntf-stand-lon-cont').show();
    $('#ntf-pole-lat-cont').show();
    return $('#ntf-pole-lon-cont').show();
  };

  get_float = function(source, container) {
    var val;
    if (container == null) {
      container = '';
    }
    val = parseFloat($(source).val());
    if (isNaN(val)) {
      $(container).addClass('error');
    } else {
      $(container).removeClass('error');
    }
    return val;
  };

  Domain = (function() {

    Domain.name = 'Domain';

    function Domain(name, width, height, dx, dy, ratio, parent_id, i_parent_start, j_parent_start) {
      this.id = NaN;
      this.name = name.trim();
      this.width = parseInt(width);
      this.height = parseInt(height);
      this.dx = parseInt(dx);
      this.dy = parseInt(dy);
      this.ratio = parseInt(ratio);
      this.parent_id = parseInt(parent_id);
      if (isNaN(this.parent_id)) {
        this.parent_id = 0;
        this.i_parent_start = 0;
        this.j_parent_start = 0;
      } else {
        this.i_parent_start = parseInt(i_parent_start);
        this.j_parent_start = parseInt(j_parent_start);
      }
    }

    Domain.prototype.assign_id = function() {
      if (isNaN(this.id)) {
        this.id = window.aqm.domain_last_id + 1;
        return window.aqm.domain_last_id = this.id;
      }
    };

    Domain.prototype.check_name = function() {
      if (this.name.length > 0) {
        return true;
      } else {
        return false;
      }
    };

    Domain.prototype.check_width = function() {
      return !isNaN(this.width);
    };

    Domain.prototype.check_height = function() {
      return !isNaN(this.height);
    };

    Domain.prototype.check_dx = function() {
      return !isNaN(this.dx);
    };

    Domain.prototype.check_dy = function() {
      return !isNaN(this.dy);
    };

    Domain.prototype.check_ratio = function() {
      return !isNaN(this.ratio);
    };

    Domain.prototype.check_i_parent_start = function() {
      return !isNaN(this.i_parent_start);
    };

    Domain.prototype.check_j_parent_start = function() {
      return !isNaN(this.j_parent_start);
    };

    Domain.prototype.check_parent_id = function() {
      if (this.parent_id === 0) {
        return false;
      } else {
        return true;
      }
    };

    Domain.prototype.check_all = function() {
      if (this.check_parent_id()) {
        if (this.check_name() && this.check_width() && this.check_height() && this.check_dx() && this.check_dy() && this.check_ratio() && this.check_ratio() && this.check_i_parent_start() && this.check_j_parent_start()) {
          return true;
        } else {
          return false;
        }
      } else {
        if (this.check_name() && this.check_width() && this.check_height() && this.check_dx() && this.check_dy() && this.check_ratio() && this.check_ratio()) {
          return true;
        } else {
          return false;
        }
      }
    };

    return Domain;

  })();

}).call(this);