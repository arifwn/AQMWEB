// Generated by CoffeeScript 1.3.1
(function() {
  var Domain, add_domain, append_parent_dropdown_list, get_domain, get_float, init_test_data, render_domain, render_domain_list, reset_domain_modal, save_domain, show_lambert_fields, show_latlon_fields, show_location_fields, show_map_modal, show_mercator_fields, show_parent_ij_field, show_polar_fields, show_preview_map;

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
    $('#ntf-parent-domain').change(function(e) {
      e.preventDefault();
      return show_parent_ij_field($('#ntf-parent-domain').val());
    });
    $('#btn-domain-modal-ok').click(function(e) {
      e.preventDefault();
      if (save_domain($('#domain-modal').attr('data-domain-id'))) {
        return $('#domain-modal').modal('hide');
      } else {
        return window.alert("Please check your input!");
      }
    });
    $('#btn-domain-modal-cancel').click(function(e) {
      e.preventDefault();
      return $('#domain-modal').modal('hide');
    });
    init_test_data();
    return render_domain_list();
  });

  render_domain_list = function() {
    var domain, _i, _len, _ref, _results;
    $('#domain-list tr[data-domain-listing]').remove();
    _ref = window.aqm.domain_list;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      domain = _ref[_i];
      _results.push(render_domain(domain));
    }
    return _results;
  };

  render_domain = function(domain) {
    var parent_domain, parent_domain_name;
    parent_domain = get_domain(domain.parent_id);
    parent_domain_name = '--';
    if (parent_domain != null) {
      parent_domain_name = parent_domain.name;
    }
    return $('#domain-list > tbody:last').append("<tr data-domain-listing=\"listing\"><td><input type=\"checkbox\" data-domain-id=\"" + domain.id + "\"></td><td><a href=\"#\" class=\"domain_link_edit\" data-domain-id=\"" + domain.id + "\">" + domain.name + "</a></td><td>" + parent_domain_name + "</td><td>" + domain.width + "</td><td>" + domain.height + "</td><td>" + domain.dx + "</td><td>" + domain.dy + "</td></tr>");
  };

  get_domain = function(domain_id) {
    var domain, _i, _len, _ref;
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
    dx = 3000;
    dy = 3000;
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
    if (isNaN(domain_id)) {
      console.log('add new domain');
      return add_domain();
    } else {
      console.log('edit existing domain');
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
    $('#ntf-dom-id').val('');
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
    console.log("mercator selected");
    $('#ntf-true-lat1-cont').show();
    $('#ntf-true-lat2-cont').hide();
    $('#ntf-stand-lon-cont').hide();
    $('#ntf-pole-lat-cont').hide();
    return $('#ntf-pole-lon-cont').hide();
  };

  show_lambert_fields = function() {
    console.log("lambert selected");
    $('#ntf-true-lat1-cont').show();
    $('#ntf-true-lat2-cont').show();
    $('#ntf-stand-lon-cont').show();
    $('#ntf-pole-lat-cont').hide();
    return $('#ntf-pole-lon-cont').hide();
  };

  show_polar_fields = function() {
    console.log("polar selected");
    $('#ntf-true-lat1-cont').show();
    $('#ntf-true-lat2-cont').hide();
    $('#ntf-stand-lon-cont').show();
    $('#ntf-pole-lat-cont').hide();
    return $('#ntf-pole-lon-cont').hide();
  };

  show_latlon_fields = function() {
    console.log("lat-lon selected");
    $('#ntf-true-lat1-cont').hide();
    $('#ntf-true-lat2-cont').hide();
    $('#ntf-stand-lon-cont').show();
    $('#ntf-pole-lat-cont').show();
    return $('#ntf-pole-lon-cont').show();
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
