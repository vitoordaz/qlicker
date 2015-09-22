(function($){
	$(function(){
		// Получение ссылки для авторизации на сервисе и переадресация по ней
		var shareLinkClicked = false;
		$('#share-links a').click(function(e){
			if (!shareLinkClicked & setBusy()) {
				shareLinkClicked = true;
				$.ajax({
					url: $(this).attr('href'),
					type: 'GET',
					success: function(data){
						location.replace(data);
					}
				});
			}
			return false;
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		// Удаление сервиса
		var nowRemoving = {};
		$('.link .remove', '#services').click(function(e){
			var href = $(this).attr('href');
			if (!(href in nowRemoving) & setBusy()) {
				nowRemoving[href] = 'removing';
				console.info(nowRemoving);
				var link = $(this).parent();
				$.ajax({
					url: href,
					type: 'GET',
					success: function(data){
						link.slideUp('slow', function(){
							$(this).remove();
							if (!$('.link', '#services').length) {
								$('#services').remove();
							}
							delete nowRemoving[href];
						});
						setNotBusy();
					}
				});
			}
			return false;
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		// Отключение отправки сообщений на сервис
		var nowToggle = {};
		$('.link .toggle', '#services').click(function(e){
			var href = $(this).attr('href');
			if (!(href in nowToggle) & setBusy()) {
				nowToggle[href] = 'toggle';
				var link = $(this);
				$.ajax({
					url: $(this).attr('href'),
					type: 'GET',
					success: function(data){
						if (link.text() == MES['On']) {
							link.text(MES['Off']);
						} else {
							link.text(MES['On']);
						}
						delete nowToggle[href];
						setNotBusy();
					}
				});
			}
			return false;
		});
	});
})(jQuery);