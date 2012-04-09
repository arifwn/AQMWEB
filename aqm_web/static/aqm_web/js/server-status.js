(function() {
  var setup_server_auto_update, update_server;

  window.setup_server_list_auto_update = function(server_list, interval) {
    var server, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = server_list.length; _i < _len; _i++) {
      server = server_list[_i];
      _results.push(setup_server_auto_update(server, interval));
    }
    return _results;
  };

  setup_server_auto_update = function(server, interval) {
    var timer, updater;
    updater = function(server) {
      return $.ajax({
        url: server.get_status_rest_url,
        dataType: "json",
        type: "GET",
        success: update_server,
        error: function(jqXHR, textStatus, errorThrown) {
          if (errorThrown === "INTERNAL SERVER ERROR") {
            $("#server_" + server.id + " > .header > .label").text("service disruption");
            $("#server_" + server.id + " > .header > .label").removeClass("label-success").addClass("label-important");
            simplebar.set("#cpu-usage-server-" + server.id, 0, "--");
            simplebar.set("#memory-usage-server-" + server.id, 0, "--");
            return simplebar.set("#disk-usage-server-" + server.id, 0, "--");
          }
        }
      });
    };
    return timer = setInterval(function() {
      return updater(server);
    }, interval);
  };

  update_server = function(server_stat) {
    var disk_label, disk_total, disk_used, memory_label, memory_total, memory_used;
    simplebar.set("#cpu-usage-server-" + server_stat.id, server_stat.cpu, "" + server_stat.cpu + "%");
    memory_used = Math.round(server_stat.memory_used / (1024 * 1024));
    memory_total = Math.round(server_stat.memory_total / (1024 * 1024));
    memory_label = "" + memory_used + " MB / " + memory_total + " MB";
    simplebar.set("#memory-usage-server-" + server_stat.id, server_stat.memory_percent, memory_label);
    disk_used = Math.round(server_stat.disk_used / (1024 * 1024 * 1024));
    disk_total = Math.round(server_stat.disk_total / (1024 * 1024 * 1024));
    disk_label = "" + disk_used + " GB / " + disk_total + " GB";
    simplebar.set("#disk-usage-server-" + server_stat.id, server_stat.disk_percent, disk_label);
    $("#server_" + server_stat.id + " > .header > .label").text("healthy");
    return $("#server_" + server_stat.id + " > .header > .label").removeClass("label-important").addClass("label-success");
  };

}).call(this);
