(function($){
	$(function(){
		/**
		 * showError --  функция для вывода ошибок формы
		 * @param {String} error текст сообщения об ошибке
		 */
		function showError(error){
			var errors = $('.submit .error', '#addLink');
			if(errors.length){
				errors.text(error).show();
			}else{
				errors = $('<div class="error fl">'+error+'</div>');
				$('.submit', '#addLink').append(errors);
			}
			setTimeout(
				function(){
					errors.fadeOut();
				}, 2000);			
		}
		
		/*-------------------------------------------------------------------------------------------*/
		
		/**
		 * Links -- класс для работы с ссылками
		 */
		function Links(){
			// Начальная инициализация
			var actColor = '#e4edf5'; // TODO: Поменять цвет
			var colorTimeout = 3000;  // 3s
			var colorAnimTime = 1000; // 1s
			
			var screen = $('#links');
			var links = $('#links-list', screen);
			var paginator = $('.paginator', screen);
			
			if(!screen.length){
				screen = $('<div id="links" class="corner c5">'+
								'<div id="links-head" class="oh">'+
									'<div class="short">'+MES['Qlinks (links)']+'</div>'+
									'<div class="clicks">'+MES['Counter']+'</div>'+
									'<div class="info">'+MES['Info']+'</div>'+
									'<div class="date">'+MES['Date']+'</div>'+
									'<div class="param">'+MES['Options']+'</div>'+
								'</div>'+
							'</div>').hide().insertAfter('#main-form');
			}
			
			if(!links.length){
				links = $('<div id="links-list"></div>').appendTo(screen);
			}
			
			if(!paginator.length){
				paginator = $('<div class="paginator">'+
								'<a class="first" href="?p=1#links"></a>' + 
								'<a class="previous" href="#links"></a>' + 
								'<div class="center">1 ' + MES['of'] + ' 1</div>'+
								'<a class="next" href="#links"></a>' +
								'<a class="last" href="#links"></a>'+
							'</div>').hide().appendTo(screen);
			}
			
			/**
			 * makeLink -- возвращает HTML код ссылки
			 * @param {Object} link -- объект ссылки
			 * 						code -- код ссылки в системе
			 * 						counter -- количество переходов
			 * 						date -- дата добавления ссылки
			 * 						favicon -- favicon страницы ссылки
			 * 						qlink -- Qlink
			 * 						title -- title страницы ссылки
			 * 						url -- номализованная ссылка (http://qliker.ru)
			 */
			var makeLink= function(link){
				link['date'] = new Date(link['date']).toLocaleFormat('%d %b');//TODO: Fix dates
				return '<div class="link oh" code="'+link['code']+'">'+
							'<div class="favicon fl"><img src="'+link['favicon']+'" alt="" title="" />&nbsp;</div>'+
							'<div class="qlink fl oh">'+
								'<div class="title oh"><a href="'+link['qlink']+'">'+link['title']+'</a></div>'+
								'<div class="long oh"><a href="'+link['url']+'">'+link['url']+'</a></div>'+
								'<div class="short oh"><a href="'+link['qlink']+'">'+link['qlink']+'</a></div>'+
							'</div>'+
							'<div class="clicks fl">'+link['counter']+'</div>'+
							'<div class="info fl"><a href="'+link['qlink']+'.info">'+MES['Info']+'</a></div>'+
							'<div class="date fl">'+link['date']+'</div>'+
							'<div class="param fl">'+
								'<span class="options">'+MES['Options']+'</span>'+
								'<ul>'+
									/*'<li><a href="#">'+MES['Copy']+'</a></li>'+*/
									'<li><a class="archivate" href="/a/archivate/'+link['code']+'">'+MES['Archive']+'</a></li>'+
									'<li><a class="edit" href="#">'+MES['Edit']+'</a></li>'+
									/*'<li><a href="#">'+MES['Share']+'</a></li>'+*/
								'</ul>'+
							'</div>'+
						'</div>';
			}
			
			/**
			 * setPage -- устанавливает состояние пагинатора
			 * @param {Intenger} curr -- текущая страница
			 * @param {Intenger} prev -- предыдущая страница
			 * @param {Intenger} next -- следующая страницы
			 * @param {Intenger} last -- последняя страница
			 */
			var setPage = function(curr, prev, next, last){
				if (last == 1){// всего одна страница
					paginator.fadeOut();
				}else{
					curPage = curr;		
					prev = (prev < 1)? 1: prev;
					next = (next > last)? last: next;
					$('.previous', paginator).attr('href', '?p=' + prev + '#links');
					$('.center', paginator).text(curr + ' ' + MES['of'] + ' ' + last);
					$('.next', paginator).attr('href', '?p=' + next + '#links');
					$('.last', paginator).attr('href', '?p='+ last +'#links');	
					paginator.fadeIn()
				}
			}
			
			/**
			 * addLinks -- добавляет ссылки
			 * @param {Object} data -- объект содержит:
			 * 					added -- массив добавленных ссылок
			 * 						qlink -- Qlink
			 * 						code -- код ссылки
			 * 						url -- исходная ссылка
			 * 					links -- массив ссылок для данной страницы (curPage)
			 * 						code -- код ссылки в системе
			 * 						counter -- количество переходов
			 * 						date -- дата добавления ссылки
			 * 						favicon -- favicon страницы ссылки
			 * 						qlink -- Qlink
			 * 						title -- title страницы ссылки
			 * 						url -- номализованная ссылка (http://qliker.ru)
			 * 					pages -- объект содержащий:
			 * 						last -- последняя страница
			 * 						previous -- предыдущая страница
			 * 						current -- текущая страница
			 * 						next -- следующая страница
			 */
			this.addLinks = function(data){
				// выводим все ссылки
				if(!data.links.length){
					return;
				}
				var html = '';
				for (link in data.links) {
					html += makeLink(data.links[link]);
				}
				if(screen.is(':hidden')){
					screen.show();
				}				
				links.html(html);
				var url_text = $('#id_url').val() || '';
				$(data.added).each(function(i){
					url_text = url_text.replace(this.url, this.qlink);
					if (curPage == 1) {
						var link = $('div[code=' + this.code + ']', links);
						if (!link.is(':animated')) {
							var prevBackgroundColor = link.css('background-color');
							link.css('background-color', actColor);								
						}
						setTimeout(function(){
							link.animate({
								backgroundColor: prevBackgroundColor
							}, colorAnimTime);
						}, colorTimeout);
					}
				});
				$('#id_url').val(url_text); 
				setPage(data.pages['current'], data.pages['previous'], data.pages['next'], data.pages['last']);
			}
			
			var addLinks = this.addLinks
			/**
			 * removeLinks -- удаляет ссылку
			 * @param {Object} code -- код ссылки
			 */
			this.removeLink = function(code){
				var link = $('.link[code='+code+']', links);
				link.slideUp('slow', function(){
					$(this).remove();
					if (!$('.link', links).length) {
						screen.hide();
					} else {
						// Обновить список ссылок
						$.getJSON('/', function(data){
							addLinks(data);
						});
					}
				});
			}
			
			// Обработчики событий
			// переход на другую страницу
			$('a', paginator).click(function(e){
				if (setBusy()) {
					$.getJSON($(this).attr('href'), function(data){
						var html = '';
						$.each(data.links, function(i){
							html += makeLink(this)
						});
						$(links).html(html);
						setPage(data.pages.current, data.pages.previous, data.pages.next, data.pages.last);
						setNotBusy();
						//document.location = '?p=' + curPage + '#links';
					});
				}
				return false;
			});
		}
		
		var links = new Links();
		
		/*-------------------------------------------------------------------------------------------*/
		
		/**
		 * Services -- класс для работы с сервисами
		 */
		function Services(){
			var screen = $('#msg-preview');
			
			if(!screen.length){
				screen = $('<div class="fr" id="msg-preview"></div>').hide().insertAfter('#addLink');
			}
			
			/**
			 * makeService -- возвращает HTML код сервиса
			 * @param {Object} service
			 */
			var makeService= function(service){
				return '<div class="service" class="oh" slug="' + service['slug'] + '">'+
							'<div class="oh">'+
								'<div class="fl" class="service-user">'+
									'<div class="service-avatar" style="background-image: url(' + service['picture'] + ');">'+
										'<div style="background-image: url(/static/' + service['ico'] + ');"></div>'+
									'</div>'+
								'</div>'+
								'<div class="fr text"></div>'+
							'</div>'+
							'<div class="counter" maxlen="' + service['mesmaxlen'] + '">' + service['mesmaxlen'] + '</div>'+
						'</div>';
			}
			/**
			 * removeService -- удаляет сервис
			 * @param {Object} slug
			 */
			this.removeService = function(slug){
				$('.service[slug='+slug+']', screen).fadeOut('normal', function(){
					$(this).remove();
					if(!$('.service', screen).length){
						screen.hide();
					}
				});
			}
			
			/**
			 * addService Функция добавляющая ссылку
			 * @param {Object} data -- объект сервиса
			 */
			this.addService = function(data){
				if (screen.is(':hidden')) {
					screen.show();
				}
				if (data['slug'] == 'twitter') {
					$(makeService(data)).hide().prependTo(screen).fadeIn();
				} else {
					$(makeService(data)).hide().appendTo(screen).fadeIn();
				}
			}
			
			/**
			 * updateServices -- обновляет превью сообщения, 
			 * которое будет отправленно в сервисы.
			 * @param {String} msg
			 */
			this.updateServices = function(msg){
				$('.service', screen).each(function(i){
					var lmsg = msg;
					var screen = $('.text', $(this));
					var counter = $('.counter', $(this));
					var maxlen = parseInt($(counter).attr('maxlen'));
					screen.removeClass('inform');
					if(lmsg.length > maxlen){
						lmsg = lmsg.slice(0, maxlen);
					}
					screen.text(lmsg);
					counter.text(maxlen - lmsg.length);
				});
			}
			
			var updateServices = this.updateServices;
			
			/**
			 * inform -- отображает результат операции
			 * @param {Object} status -- объект, содержащий результаты операций для каждого сервиса
			 */
			this.inform = function(status){
				for (i in status) {
					$('.service[slug=' + i + '] .text', screen).addClass('inform').text(MES[status[i]]);
				}				
			}
		}
		
		var services = new Services();
		
		/*-------------------------------------------------------------------------------------------*/
		
		//Нажатие на кнопку сокращение
		$('#short', '#addLink').click(function(e){
			$('.param', '#links').removeClass('clicked');
			var form = $('#addLink');
			var isError = $(form).is('.error');
			if(!isError & !checkBusy()){
				//Проверка ссылки
				var url = $('#id_url', form);
				url.trigger('blur');//снимаем фокус
				if (url.val() == '') {
					showError(MES['Require url']);
					isError = true;
				}else if(isQlink(url.val())){
					showError(MES['Alredy Qlink']);
					isError = true;
				}else if(!isThereUrl(url.val())){
					showError(MES['Wrong url']);
					isError = true;
				}
				if(isError){
					url.addClass('wrong');
					setTimeout(
						function(){
							url.removeClass('wrong');
						}, 2000
					);	
					return false;
				}
				//отправляем ссылку
				if (setBusy()) {
					$('#id_url').attr('disabled', 'disabled');
					$.ajax({
						url: $(form).attr('action') + '?p=' + curPage,
						type: $(form).attr('method'),
						data: {
							'url': url.val(),
							'short': 'short',
							'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
						},
						dataType: 'json',
						success: function(data){
							if (data['error']) {
								url.addClass('wrong');
								showError(data['error']['url'][0]);
								isError = true;
								setTimeout(
									function(){
										url.removeClass('wrong');
									}, 2000
								);	
							} else {
								links.addLinks(data);
							}
							setNotBusy();
							$('#id_url').removeAttr('disabled');
						}
					});
				}
			}
			return false;
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		// Нажатие на кнопку поделиться
		$('#share', '#addLink').click(function(e){
			$('.param', '#links').removeClass('clicked');
			var form = $('#addLink');
			var isError = false;
			if(!isError & !checkBusy()){
				// Проверка сообщения
				var url = $('#id_url', form);
				url.trigger('blur');// снимаем фокус
				if (url.val() == '') {
					showError(MES['Require message']);
					isError = true;
				}
				if (!$('.service', '#msg-preview').length) {
					showError(MES['Active service']);
					isError = true;
				}
				if(isError){
					url.addClass('wrong');
					setTimeout(
						function(){
							url.removeClass('wrong');
						}, 2000
					);	
					return false;
				}
				// отправляем сообщение
				if (setBusy()) {
					$('#id_url').attr('disabled', 'disabled');
					$.ajax({
						url: $(form).attr('action') + '?p=' + curPage,
						type: $(form).attr('method'),
						data: {
							'url': url.val(),
							'share': 'share',
							'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
						},
						dataType: 'json',
						success: function(data){
							if (data['error']) {
								url.addClass('wrong');
								showError(data['error']['url'][0]);
								isError = true;
							} else {
								links.addLinks(data);
								services.inform(data['status']);
							}
							setNotBusy();
							$('#id_url').removeAttr('disabled');
						}
					});
				}
			}
			return false;
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		// Отключение отправки сообщений на сервис
		var nowToggle = {};
		$('li .service-link', '#user-services').click(function(e){
			$('.param', '#links').removeClass('clicked');
			var href = $(this).attr('href');
			if (!(href in nowToggle) & !checkBusy()) {
				nowToggle[href] = 'toggle';
				var link = $(this);
				if (setBusy()) {
					$.ajax({
						url: $(this).attr('href'),
						type: 'GET',
						dataType: 'json',
						success: function(data){
							var title = link.attr('title').split(' - ', 1);
							var slug = link.attr('slug');
							if (data) {
								services.addService(data);
								services.updateServices($('#id_url').val());
								link.removeClass('inactive');
								link.attr('title', title + ' - ' + MES['active']);
								link.attr('alt', title + ' - ' + MES['active'])
							} else {
								services.removeService(slug);
								link.addClass('inactive');
								link.attr('title', title + ' - ' + MES['inactive']);
								link.attr('alt', title + ' - ' + MES['inactive'])
							}
							delete nowToggle[href];
							setNotBusy();
						}
					});
				}
			}
			return false;
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		// Обновление превью сообщения
		$('#id_url').keypress(function(e){
			if (e.charCode == 32) {/*space code*/
				var urlVal = e.target.value;
				if (urlVal) {
					var urlar = urlVal.split(' ');
					var linksForShort = [];
					for (i in urlar) {
						if (isUrl(urlar[i]) && !isQlink(urlar[i])) {
							linksForShort.push(urlar[i]);
						}
					}
					if(linksForShort.length){
						// укорачиваем ссылки
						var url = $(this);
						var form = $('#addLink');
						url.addClass('busy');
						$.ajax({
							url: $(form).attr('action') + '?p=' + curPage,
							type: $(form).attr('method'),
							data: {
								'url': urlVal,
								'short': 'short',
								'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
							},
							dataType: 'json',
							success: function(data){
								links.addLinks(data);
								// TODO: возможно так лучше это надо обсудить
								/*var newUrlVal = url.val();
								if (data.added.length) {
									$(data.added).each(function(i){
										newUrlVal = newUrlVal.replace(this.url, this.qlink);
									});
								}
								url.val(newUrlVal);*/
								url.removeClass('busy');
							}
						});
					}
				}
			}
		});
		
		$('#id_url').keyup(function(e){
			var msg = $(this).val();
			services.updateServices($(this).val());
		});
		
		$('#id_url').change(function(e){
			services.updateServices($(this).val());
		});
		
		$('#id_url').click(function(e){
			services.updateServices($(this).val());
			$('.param', '#links').removeClass('clicked');
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		$('body').click(
			function(e){
				if (e.target.textContent != MES['Options']) {
					$('.param.clicked', '#links').removeClass('clicked');
				}
			}
		);
		
		// Установки
		$('.param', '#links').live('click',
			function(e){
				var clicked = $(this).hasClass('clicked');
				$('.param', '#links').removeClass('clicked');
				if (!clicked) {
					$(this).addClass('clicked');
				}
				return false;
			}
		);
		
		// Архивировать
		$('.param ul li .archivate', '#links').live('click',
			function(e){
				var code = $(this).parents('.link').attr('code');
				if (!checkBusy()) {
					if (setBusy()) {
						$.ajax({
							url: $(this).attr('href'),
							data: {'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]', '#addLink').val()},
							type: 'POST',
							dataType: 'text',
							success: function(data){
								links.removeLink(code);
								setNotBusy();
							}
						});
					}
				}
				$(this).parents('.param').removeClass('clicked');
				return false;
			}
		);
		
		// Редактировать
		$('.param ul li .edit', '#links').live('click',
			function(e){
				var link = $(this).parents('.link');
				var code = link.attr('code');
				var title = $('.title', link);
				if ($('a', title).length) {
					var form = '<form class="title-edit" method="post" action="/a/edit/' + link.attr('code') + '">' +
									'<div style="display: none;"><input type="hidden" value="' + $('[name=csrfmiddlewaretoken]', '#addLink').val() + '" name="csrfmiddlewaretoken"></div>' +
									'<input type="text" name="title" value="' + title.text() + '"/>' + 
									'<input type="submit" value="' + MES['Save'] + '"/>' +
								'</form>';
					title.html(form);
				}
				return false;
			}
		);
		
		// Форма редактирования заголовков ссылок
		$('.title-edit', '#links').live('submit', function(e){
			$.ajax({
				url: $(this).attr('action'),
				type: $(this).attr('method'),
				data: $(this).serialize(),
				dataType: 'text'
			});
			var title = $('input[name=title]', $(this)).val();
			$(this).parent().html('<a href="/'+$(this).parents('.link').attr('code')+'">'+title+'</a>');
			return false;
		});
	});
})(jQuery);