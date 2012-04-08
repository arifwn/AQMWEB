(function() {
  var append_task, get_task_html, setup_task_auto_update;

  window.render_task_list = function(target, task_list) {
    var task, _i, _len, _results;
    console.log(task_list);
    _results = [];
    for (_i = 0, _len = task_list.length; _i < _len; _i++) {
      task = task_list[_i];
      _results.push(append_task(target, task));
    }
    return _results;
  };

  window.update_task = function(task) {
    var task_html;
    task_html = get_task_html(task);
    $("#task-" + task.id).empty();
    return $("#task-" + task.id).append(task_html);
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
    var timer, updater;
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
    return timer = setInterval(function() {
      return updater(task);
    }, interval);
  };

  append_task = function(target, task) {
    var html, task_html;
    task_html = get_task_html(task);
    html = "<li id=\"task-" + task.id + "\">\n    " + task_html + "\n</li>";
    return $(target).append(html);
  };

  get_task_html = function(task) {
    var controls_html, html, progress_html;
    controls_html = "";
    progress_html = "";
    if (task.get_status === "draft") {
      controls_html = "<li><a class=\"btn btn-info\" href=\"#\">Run</a></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label\">draft</span></div>";
    } else if (task.get_status === "pending") {
      controls_html = "        <li><a class=\"btn btn-danger\" href=\"#\">Cancel</a></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>";
      progress_html = "<div class=\"counter warning\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-warning\">pending</span></div>";
    } else if (task.get_status === "running") {
      controls_html = "        <li><a class=\"btn btn-danger\" href=\"#\">Stop</a></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>";
      progress_html = "<div class=\"counter info\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-info\">running</span></div>\n<div class=\"progress progress-striped active\">\n    <div class=\"bar\" style=\"width: 30%;\"></div>\n</div>";
    } else if (task.get_status === "finished") {
      controls_html = "<li><a class=\"btn btn-success\" href=\"#\">Results</a></li>\n<li><a class=\"btn btn-info\" href=\"#\">Run Again</a></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter success\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-success\">finished</span></div>";
    } else if (task.get_status === "error") {
      controls_html = "<li><a class=\"btn btn-info\" href=\"#\">Retry last stage</a></li>\n<li><a class=\"btn btn-info\" href=\"#\">Run</a></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter important\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-important\">error</span></div>";
    } else if (task.get_status === "canceled") {
      controls_html = "<li><a class=\"btn btn-info\" href=\"#\">Resume from last stage</a></li>\n<li><a class=\"btn btn-info\" href=\"#\">Run</a></li>\n<li><a class=\"btn\" href=\"#\">Details</a></li>\n<li><a class=\"btn\" href=\"#\">Edit</a></li>\n<li><a class=\"btn btn-danger\" href=\"#\">Delete</a></li>";
      progress_html = "<div class=\"counter important\">" + task.get_progress_percent + "%</div>\n<div class=\"stage\">" + task.get_stage + "</div>\n<div><span class=\"label label-important\">canceled</span></div>";
    }
    return html = "<div class=\"header\">\n    <h2><a href=\"#\">" + task.name + "</a></h2>\n</div>\n<div class=\"content\">\n    <div class=\"well\">\n    " + task.description + "\n    </div>\n    <table class=\"table table-striped table-bordered table-condensed\">\n        <thead>\n            <tr>\n                <th>User</th>\n                <th>Domain</th>\n                <th>Period</th>\n            </tr>\n        </thead>\n        <tbody>\n            <tr>\n                <td><a href=\"/accounts/profile/" + task.user.username + "\"><img class=\"avatar\" src=\"/accounts/avatar/t32x32/" + task.user.username + "\" width=\"32\" height=\"32\" style=\"height: 32px;\" /></a> <a href=\"/accounts/profile/" + task.user.username + "\">" + task.user.get_full_name + " (" + task.user.username + ")</a></td>\n                <td>" + task.setting.get_max_dom + "</td>\n                <td>" + task.setting.get_start_date + " &mdash; " + task.setting.get_end_date + "</td>\n            </tr>\n        </tbody>\n    </table>\n    <ul class=\"controls\">\n        " + controls_html + "\n    </ul>\n</div>\n\n<div class=\"task-progress\">\n    " + progress_html + "\n</div>";
  };

}).call(this);
