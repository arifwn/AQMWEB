
var simplebar = {};

simplebar.create = function(target){
	var percentage = $(target).attr('data-simplebar-percentage');
	var label = $(target).attr('data-simplebar-text');
	if (percentage !== undefined){
		$(target).find('.bar').attr('style', 'width: '+percentage+'%;');
	}
	if (label !== undefined){
		$(target).find('.inner-text').text(label);
	}
};

simplebar.set = function(target, percentage, label){
	$(target).attr('data-simplebar-percentage');
	$(target).attr('data-simplebar-text');
	if (percentage !== undefined){
//		$(target).find('.bar').attr('style', 'width: '+percentage+'%;');
		if (percentage > 100) percentage = 100;
		$(target).find('.bar').animate({width: percentage+'%'}, 2000, 'linear');
	}
	if (label !== undefined){
		$(target).find('.inner-text').text(label);
	}
};

(function( $ ){
	var simplebar_html = '<div class="inner-bar"><div class="bar"></div></div><div class="inner-text"></div>';
	
	$(document).ready(function () {
		$('[data-simplebar]').simplebar();
	});
	
	$.fn.simplebar = function ( selector ) {
		return this.each(function() {
			$(this).html(simplebar_html);
			$(this).addClass('bar-chart');
			simplebar.create(this);
			
		});
	};
	
	
})( window.jQuery || window.ender )