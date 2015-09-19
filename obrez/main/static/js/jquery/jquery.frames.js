/**
 * Frames plugin
 * @author Victor Rodionov <vito.ordaz@gmail.com>
 * @param {String} show -- фрейм который нужно показать
 * @param {Boolean} back -- флаг показывающий что страница 
 * @param {Object} o -- опции
 */
(function($){
	$(function(){
		$.fn.frames = function(show, back, o){
			var o = $.extend({
				interval:	500,
				cframe:		'#cframe',		//центральный фрэйм
				lframe:		'#lframe',		//левый фрэйм
				rframe:		'#rframe',		//правый фрэйм
				bframe:		'#bframe',		//нижний фрэйм
				content:	$('#content')	//объемлющий фрэйм
			}, o);
			var opt = {};
			switch(show){
				case 'rframe':
					if(back)
						opt = {left: '+=100%'};
					else
						opt = {left: '-=100%'};
				break;
				case 'lframe':
					if(back)
						opt = {left: '-=100%'};
					else
						opt = {left: '+=100%'};
				break;
				case 'bframe':
					if(back)
						opt = {top: '+=100%'};
					else
						opt = {top: '-=100%'};
				break; 
			}
		    $(this).click(function(e){
				o.content.addClass('oh');
				var go = $(o[show]+' .go').hide();
		      	$(o.cframe+','+o[show]).show().animate(
					opt, 
					o.interval,
					function(){
						if(back){
							$(o[show]).hide();
						}else{
							$(o.cframe).hide();
						}
						go.fadeIn(o.interval);
						o.content.removeClass('oh');
					}
				);
				return false;
			});
		};
	});
})(jQuery);
