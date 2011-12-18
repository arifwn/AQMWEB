/* ============================================================
 * Stream Gallery 0.1.0
 * A jQuery plugin which provides gallery elements
 * ============================================================
 * 
 * Arif Widi Nugroho <arif@sainsmograf.com>
 * ============================================================ */

var stream_gallery = {};

stream_gallery.next = function(gallery_id){
	var target = stream_gallery[gallery_id].num + 1;
	if(target > stream_gallery[gallery_id].maxnum){
		target = 1;
	}
	
//	console.log('next: ' + target);
	stream_gallery.goto_target(gallery_id, target);
};

stream_gallery.prev = function(gallery_id){
	var target = stream_gallery[gallery_id].num - 1;
	if(target < 1){
		target = stream_gallery[gallery_id].maxnum;
	}
	
//	console.log('prev: ' + target);
	stream_gallery.goto_target(gallery_id, target);
};

stream_gallery.goto_target = function(gallery_id, target){
//	console.log('goto ' + target);
	
	// display target item
	var item_width = $('#'+gallery_id+' .viewport .viewlist li').outerWidth();
	var left = item_width * (target - 1);
	$('#'+gallery_id+' .viewport .viewlist').css({
		'left' : '-' + left + 'px'
	});
	
	// update statusbar
	var description = $('#'+gallery_id+' .viewport .viewlist li[data-stream-gallery-num='+target+']').attr('data-item-description');
	$('#'+gallery_id+' .statusbar .description').html(description);
	
	stream_gallery[gallery_id].num = target;
	stream_gallery.highlight_target(gallery_id, target);
};

stream_gallery.highlight_target = function(gallery_id, target){

	var item_height = $('#'+gallery_id+' .navigation .navlist li').outerHeight();
	var navigation_height = $('#'+gallery_id+' .navigation').outerHeight();
	
	// highlight item's navigation list
	$('#'+gallery_id+' .navigation .navlist li a').removeClass('active');
	$('#'+gallery_id+' .navigation .navlist li a[data-stream-gallery-num='+target+']').addClass('active');
	
	var current_len = item_height * target;
	var offset = (((current_len - navigation_height) / item_height) + 1) * item_height;
	var position = $('#'+gallery_id+' .navigation .navlist').position();
	
	$('#'+gallery_id+' .navigation .navlist').stop(true, true);
	
	if(current_len > navigation_height){
//		$('#'+gallery_id+' .navigation .navlist').animate({
//			'top' : '-' + offset + 'px'
//		}, 300);
		$('#'+gallery_id+' .navigation .navlist').scrollTop(offset);
	}
	else if(position.top !== 0){
//		$('#'+gallery_id+' .navigation .navlist').animate({
//			'top' : '0'
//		}, 300);
		$('#'+gallery_id+' .navigation .navlist').scrollTop(0);
	}

};

(function( $ ){
	
	var stream_gallery_num = 0;
	
	$(document).ready(function () {
		$('[data-stream-gallery]').stream_gallery()
	});
	
	
	/* CAROUSEL PLUGIN DEFINITION
	 * ========================== */
	$.fn.stream_gallery = function ( selector ) {
		return this.each(function() {
			var id_name = $(this).attr('id');
			
			if(id_name===undefined){
				//No id? Do not fear! let's give it one! 
				id_name = 'news_carousel_'+stream_gallery_num;
				$(this).attr('id', id_name);
				stream_gallery_num++;
			}
			
			stream_gallery[id_name] = {
					maxnum : $('#'+id_name+' .viewport .viewlist li').length,
					num : 1,
					play_interval : 1000,
					play_timer: null,
					is_playing: false
				};
			
			//assign an event handler
			var next_btn = $('#' + id_name + ' .playcontrol .next');
			var prev_btn = $('#' + id_name + ' .playcontrol .prev');
			var play_btn = $('#' + id_name + ' .playcontrol .play');
			var pause_btn = $('#' + id_name + ' .playcontrol .pause');
			
			next_btn.click(function(e){
		        e.preventDefault();
		        // next action
		        console.log('next');
		        stream_gallery.next(id_name);
		    });

			prev_btn.click(function(e){
		        e.preventDefault();
		        // prev action
		        stream_gallery.prev(id_name);
		    });

			play_btn.click(function(e){
		        e.preventDefault();
		        // play action
		        stream_gallery.next(id_name);
		        
		        stream_gallery[id_name].play_timer = setInterval(function(){
		        	stream_gallery.next(id_name);
		        }, stream_gallery[id_name].play_interval);
		        stream_gallery[id_name].is_playing = true;
		        
//		        console.log('play');
		        play_btn.hide();
		        pause_btn.show();
		    });

			pause_btn.click(function(e){
		        e.preventDefault();
		        // pause action
		        
		        clearInterval(stream_gallery[id_name].play_timer);
		        stream_gallery[id_name].is_playing = false;
		        
//		        console.log('pause');
		        play_btn.show();
		        pause_btn.hide();
		    });
			
			//list navigation
			$('#'+id_name+' .navigation .navlist li a').click(function(e){
		        e.preventDefault();
		        var target_num = parseInt($(this).attr('data-stream-gallery-num'));
		        // display targetted image
		        stream_gallery.goto_target(id_name, target_num);
		    });
			
			//setup global navigation key
			if($(this).attr('data-stream-galery-enable-hotkey')===undefined){
				console.log('no hotkey for: '+id_name);
			}
			else {
				console.log('hotkey for ' + id_name);
				$(document).keydown(function(e){
					if(e.which === 39){
				        stream_gallery.next(id_name);
					}
					else if(e.which === 37){
				        stream_gallery.prev(id_name);
					}
					else if(e.which === 13){
//						console.log('hotkey enter');
						if(stream_gallery[id_name].is_playing){
							pause_btn.click();
						}
						else {
							play_btn.click();
						}
					}
				});
			}
			
			//setup first view
			var description = $('#'+id_name+' .viewport .viewlist li[data-stream-gallery-num=1]').attr('data-item-description');
			$('#'+id_name+' .statusbar .description').html(description);
			
			//setup play mode
			var interval = parseInt($(this).attr('data-stream-gallery-play-interval'));
			if (isNaN(interval)){
//				alert('oh no its NaN!');
			}
			else {
				stream_gallery[id_name].play_interval = interval;
				console.log('custom play interval: ' + interval);
			}
			
		});
	};
	
})( window.jQuery || window.ender )