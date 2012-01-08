$(document).ready(function(){
	var toolbox_pos = {};
	toolbox_pos.top = $('#toolbox').offset().top - 40;
	toolbox_pos.left = $('#toolbox').offset().left;
	
	$(window).scroll(function(){
		var scroll_pos = $(window).scrollTop();
		if (scroll_pos > toolbox_pos.top) {
			$('#toolbox').addClass('fixed');
		}
		else if (scroll_pos < toolbox_pos.top) {
			$('#toolbox').removeClass('fixed');
		}
	});

});
