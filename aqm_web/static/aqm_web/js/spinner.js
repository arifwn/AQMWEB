
var spinner_func = {};
var spinners = {length: 0};

spinner_func.spinner_animate = function(target){
	var target_key = 'spinner_'+(spinners.length++);
	spinners[target_key] = {};
	if($(target).attr('id')===undefined){
		$(target).attr('id', target_key);
		spinners[target_key].id = target_key;
	}
	else {
		spinners[target_key].id = $(target).attr('id');
	}
	$(target).attr('data-spinner-key', target_key);
	spinners[target_key].arrow_active = 0;
	spinners[target_key].arrow_num = $(target).children().length;
	spinners[target_key].anim_interval = 100;

	var id = spinners[target_key].id;
	spinners[target_key].anim_timer = setInterval(function(){
		var i = spinners[target_key].arrow_active + 1;
		if (i >= spinners[target_key].arrow_num) i = 0;
		var previous_target = $('#'+id).children()[spinners[target_key].arrow_active];
    	var target = $('#'+id).children()[i];

    	$(previous_target).removeClass('active');
    	$(target).addClass('active');
    	
    	spinners[target_key].arrow_active = i;
    }, spinners[target_key].anim_interval);
	
	
};

spinner_func.spinner_create = function(target){
	var target_key = 'spinner_'+(spinners.length++);
	spinners[target_key] = {};
	if($(target).attr('id')===undefined){
		$(target).attr('id', target_key);
		spinners[target_key].id = target_key;
	}
	else {
		spinners[target_key].id = $(target).attr('id');
	}
	$(target).attr('data-spinner-key', target_key);
	spinners[target_key].arrow_active = 0;
	spinners[target_key].arrow_num = $(target).children().length;
	spinners[target_key].anim_interval = 100;
	
	spinners[target_key].anim_timer = null;
	
	
};

spinner_func.spinner_play_by_key = function(target_key){
	var id = spinners[target_key].id;
	spinners[target_key].anim_timer = setInterval(function(){
		var i = spinners[target_key].arrow_active + 1;
		if (i >= spinners[target_key].arrow_num) i = 0;
		var previous_target = $('#'+id).children()[spinners[target_key].arrow_active];
    	var target = $('#'+id).children()[i];

    	$(previous_target).removeClass('active');
    	$(target).addClass('active');
    	
    	spinners[target_key].arrow_active = i;
    }, spinners[target_key].anim_interval);
	
	
};

spinner_func.spinner_play = function(query){
	var key = $(query).attr('data-spinner-key');
	if(key!==undefined){
		spinner_func.spinner_play_by_key(key);
	}
};

spinner_func.spinner_stop_by_key = function(target_key){
	console.log('stop:', target_key);
	clearInterval(spinners[target_key].anim_timer);
};

spinner_func.spinner_stop = function(query){
	var key = $(query).attr('data-spinner-key');
	if(key!==undefined){
		spinner_func.spinner_stop_by_key(key);
	}
};

spinner_func.spinner_activate = function(){
	var spinner_html = '<div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div>';
	var targets = $('[data-spinner]');
	targets.html(spinner_html);
	for(var i=0; i<targets.length; i++){
		var target = targets[i];
		$(targets[i]).addClass('spinner');
		if($(target).attr('data-spinner')==='noauto'){
			spinner_func.spinner_create($(targets[i]));
		}
		else {
			spinner_func.spinner_animate($(targets[i]));
		}
	}
	
};

(function( $ ){
	var spinner_html = '<div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div> <div class="arrow"></div>';
	
	$(document).ready(function () {
		$('[data-spinner]').spinner_control()
	});
	
	$.fn.spinner_control = function ( selector ) {
		return this.each(function() {
			$(this).html(spinner_html);
			$(this).addClass('spinner');
			if($(this).attr('data-spinner')==='noauto'){
				spinner_func.spinner_create($(this));
			}
			else {
				spinner_func.spinner_animate($(this));
			}
		});
	};
	
})( window.jQuery || window.ender )
