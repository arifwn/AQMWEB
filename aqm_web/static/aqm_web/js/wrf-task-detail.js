// Generated by CoffeeScript 1.3.1
(function() {

  window.render_result_browser = function(target_id, data_list) {
    var data, html, i, _i, _len, _results;
    $("" + target_id + " .viewport .viewlist").empty();
    i = 1;
    _results = [];
    for (_i = 0, _len = data_list.length; _i < _len; _i++) {
      data = data_list[_i];
      html = "<li data-item-description=\"" + data.description + "\" data-stream-gallery-num=\"" + i + "\">\n    <img class=\"view-item\" src=\"" + data.url + "\" />\n</li>";
      $("" + target_id + " .viewport .viewlist").append(html);
      _results.push(i += 1);
    }
    return _results;
  };

  window.update_log_wrf = function(task_id) {
    var real_log, real_log_html, wrf_log, wrf_log_html;
    real_log = 'just "test"';
    real_log_html = prettyPrintOne(real_log, 'js', true);
    $('#real-exe-log').empty();
    $('#real-exe-log').append(real_log_html);
    wrf_log = 'just "test"';
    wrf_log_html = prettyPrintOne(wrf_log, 'js', true);
    $('#wrf-exe-log').empty();
    return $('#wrf-exe-log').append(wrf_log_html);
  };

}).call(this);
