(function() {
  var append_task, get_task_html, setup_task_auto_update;

  window.task_list_timers = [];

  window.task_list_data = [];

  window.task_command_url = '';

  window.reset_task_list = function(target) {
    var loading_html, timer, _i, _len, _ref;
    _ref = window.task_list_timers;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      timer = _ref[_i];
      clearInterval(timer);
    }
    window.task_list_timers = [];
    $(".toolbox .nav > li").removeClass("active");
    $("#filter-all").parent().addClass("active");
    loading_html = "<li>\n    <div class=\"alert alert-info\">\n        <p>Loading...</p>\n    </div>\n</li>";
    $(target).empty();
    return $(target).append(loading_html);
  };

  window.render_task_list = function(target, task_list) {
    var task, _i, _len, _results;
    window.task_list_data = task_list;
    _results = [];
    for (_i = 0, _len = task_list.length; _i < _len; _i++) {
      task = task_list[_i];
      _results.push(append_task(target, task));
    }
    return _results;
  };

  window.reinit_event_handler = function(task) {
    $("#task-" + task.id + " .control-run").click(function(e) {
      var button;
      button = this;
      return task_command('run', task, button);
    });
    $("#task-" + task.id + " .control-rerun").click(function(e) {
      var button;
      button = this;
      return task_command('rerun', task, button);
    });
    $("#task-" + task.id + " .control-retry").click(function(e) {
      var button;
      button = this;
      return task_command('retry', task, button);
    });
    $("#task-" + task.id + " .control-stop").click(function(e) {
      var button;
      button = this;
      return task_command('stop', task, button);
    });
    return $("#task-" + task.id + " .control-cancel").click(function(e) {
      var button;
      button = this;
      return task_command('cancel', task, button);
    });
  };

  window.update_task = function(task) {
    var task_html;
    task_html = get_task_html(task);
    $("#task-" + task.id).empty();
    $("#task-" + task.id).append(task_html);
    return window.reinit_event_handler(task);
  };

  window.setup_task_list_auto_update = function(task_list, interval) {
    var task, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = task_list.length; _i < _len; _i++) {
      task = task_list[_i];
      _results.push(setup_task_auto_update(task, interval));
    }
    return _results;
  };

  setup_task_auto_update = function(task, interval) {
    var real_interval, timer, updater;
    updater = function(task) {
      return $.ajax({
        url: task.get_rest_url,
        dataType: "json",
        type: "GET",
        success: update_task,
        error: function(jqXHR, textStatus, errorThrown) {
          return console.log(errorThrown);
        }
      });
    };
    real_interval = 0;
    if (task.get_status === "running") {
      real_interval = interval;
    } else if (task.get_status === "running") {
      real_interval = 3 * interval;
    } else {
      real_interval = 10 * interval;
    }
    timer = setInterval(function() {
      return updater(task);
    }, real_interval);
    return window.task_list_timers.push(timer);
  };

  append_task = function(target, task) {
    var html, task_html;
    task_html = get_task_html(task);
    html = "<li id=\"task-" + task.id + "\">\n    " + task_html + "\n</li>";
    $(target).append(html);
    return window.reinit_event_handler(task);
  };

  get_task_html = function(task) {
    var controls_html, html, progress_html;
    controls_html = "";
    progress_html = "";
    if (task.get_status === "draft") {
      controls_html = "<li><button class=\"btn btn-info control-run\">Run</button></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label\">draft</span></div>";
    } else if (task.get_status === "pending") {
      controls_html = "        <li><button class=\"btn btn-danger control-cancel\">Cancel</button></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>";
      progress_html = "<div class=\"counter warning\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-warning\">pending</span></div>";
    } else if (task.get_status === "running") {
      controls_html = "        <li><button class=\"btn btn-danger control-stop\">Stop</button></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>";
      progress_html = "<div class=\"counter info\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-info\">running</span></div>\n<div class=\"progress progress-striped active\">\n    <div class=\"bar\" style=\"width: 30%;\"></div>\n</div>";
    } else if (task.get_status === "finished") {
      controls_html = "<li><a class=\"btn btn-success\" href=\"#\">Results</a></li>\n<li><button class=\"btn btn-info control-rerun\">Run Again</button></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter success\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-success\">finished</span></div>";
    } else if (task.get_status === "error") {
      controls_html = "<li><button class=\"btn btn-info control-retry\">Retry last stage</button></li>\n<li><button class=\"btn btn-info control-run\">Run</button></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter important\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-important\">error</span></div>";
    } else if (task.get_status === "canceled") {
      controls_html = "<li><button class=\"btn btn-info control-retry\">Resume from last stage</button></li>\n<li><button class=\"btn btn-info control-run\">Run</button></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter important\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-important\">canceled</span></div>";
    }
    return html = "<div class=\"header\">\n    <h2><a href=\"#\">" + task.name + "</a></h2>\n</div>\n<div class=\"content\">\n    <div class=\"well\">\n    " + task.description + "\n    </div>\n    <table class=\"table table-striped table-bordered table-condensed\">\n        <thead>\n            <tr>\n                <th>User</th>\n                <th>Domain</th>\n                <th>Period</th>\n            </tr>\n        </thead>\n        <tbody>\n            <tr>\n                <td><a href=\"/accounts/profile/" + task.user.username + "\"><img class=\"avatar\" src=\"/accounts/avatar/t32x32/" + task.user.username + "\" width=\"32\" height=\"32\" style=\"height: 32px;\" /></a> <a href=\"/accounts/profile/" + task.user.username + "\">" + task.user.get_full_name + " (" + task.user.username + ")</a></td>\n                <td>" + task.setting.get_max_dom + "</td>\n                <td>" + task.setting.get_start_date + " &mdash; " + task.setting.get_end_date + "</td>\n            </tr>\n        </tbody>\n    </table>\n    <ul class=\"controls\">\n        " + controls_html + "\n    </ul>\n</div>\n\n<div class=\"task-progress\">\n    " + progress_html + "\n</div>";
  };

  window.filter_display = function(task_list, filter) {
    var filter_display, task, _i, _len, _ref, _results;
    $(".toolbox .nav > li").removeClass("active");
    $("#filter-" + filter).parent().addClass("active");
    $('html, body').animate({
      scrollTop: 0
    }, 300);
    filter_display = function(task) {
      if (filter === "all") {
        return $("#task-" + task.id).removeClass("hidden");
      } else {
        if (task.get_status === filter) {
          return $("#task-" + task.id).removeClass("hidden");
        } else {
          return $("#task-" + task.id).addClass("hidden");
        }
      }
    };
    _ref = window.task_list_data;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      task = _ref[_i];
      _results.push(filter_display(task));
    }
    return _results;
  };

  window.task_command = function(command, task, button) {
    $(button).button('toggle');
    return $.ajax({
      url: window.task_command_url,
      dataType: "json",
      type: "POST",
      data: {
        task_id: task.id,
        command: command
      },
      success: function(data) {
        $(button).button('toggle');
        if (data.success) {
          $.ajax({
            url: task.get_rest_url,
            dataType: "json",
            type: "GET",
            success: update_task
          });
          $.ajax({
            url: window.task_list_url,
            dataType: "json",
            type: "GET",
            success: function(data) {
              var timer, _i, _len, _ref;
              _ref = window.task_list_timers;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                timer = _ref[_i];
                clearInterval(timer);
              }
              window.task_list_timers = [];
              window.task_list_data = data;
              window.setup_task_list_auto_update(data, 5000);
              return console.log("timer updated!");
            }
          });
          return console.log("operation succeed!");
        } else {
          return window.aqm.alert("Error", data.message);
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        $(button).button('toggle');
        return window.aqm.alert("Error", "Connection Failed: " + textStatus + " " + errorThrown);
      }
    });
  };

}).call(this);
