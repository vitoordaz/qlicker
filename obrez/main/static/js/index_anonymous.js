(function($){
	$(function(){
		$('#go_l').frames('lframe', false);
		$('#go_lc').frames('lframe', true);
		
		$('#go_r').frames('rframe', false);
		$('#go_rc').frames('rframe', true);
		
		$('#go_b').frames('bframe', false);
		$('#go_bc').frames('bframe', true);
		
		$('#auth-btn').toggle(
			function(e){
				$('#auth-form').fadeIn();
			},
			function(e){
				$('#auth-form').fadeOut();
			}
		);
		
		/*-------------------------------------------------------------------------------------------*/
		
		/**
		 * Links -- класс для работы с ссылками
		 */
		function Links(){
			var actColor = '#e4edf5';//TODO: Поменять цвет
			var colorTimeout = 3000;//3s
			var colorAnimTime = 1000;//1s
			var perPage = 10;//ссылок на страницу
			
			var screen = $('#links');
			var links = $('#links-list', screen);
			var paginator = $('.paginator', screen);
	
			if(!screen.length){
				screen = $('<div id="links" class="corner c5">'+
								'<div id="links-head" class="oh">'+
									'<div class="short">'+MES['New link']+'</div>'+
									'<div class="long">'+MES['Long link']+'</div>'+
								'</div>'+
							'</div>').hide().insertAfter('#main-input');
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
			 * @param {String} code -- код укороченной ссылки
			 * @param {String} url -- ссылка на полную версию ссылки
			 * @return {String}
			 */
			var makeLink= function(code, url){
				return '<div class="link oh" code="'+code+'">'+
							'<div class="short"><a href="http://'+HOST+code+'">http://'+HOST+code+'</a></div>'+
								'<div class="params">'+
									'<a href="http://'+HOST+code+'.info" class="stat-l">'+MES['Info']+'</a><a href="#">'+MES['Copy']+'</a>'+
								'</div>'+
							'<div class="long"><a href="'+url+'">'+url+'</a></div>'+
						'</div>';
			}
			
			/**
			 * setPage -- устанавливает текущую страницу
			 * @param {Intenger} page -- текущая страница
			 */
			var setPage = function(curr, prev, next, last){
				if (last != 1){
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
			 * addLink Функция добавляющая ссылку
			 * @param {Object} obj -- объект ссылка содержит: code - код укороченной версии ссылки, url - длинная ссылка
			 */
			this.addLink = function(obj, pages){
				if(curPage == 1){
					var link = $(links).find('div[code=' + obj['code'] + ']');
					if(link.length){
						if(!link.is(':animated')){
							var prevBackgroundColor = link.css('background-color');
							link.css('background-color', actColor);
							setTimeout(function(){
								link.animate({
									backgroundColor: prevBackgroundColor
								}, colorAnimTime);
							}, colorTimeout);
						}
					}else{
						link = $(makeLink(obj['code'], obj['url'])).prependTo(links).hide();
						if(screen.is(':hidden')){
							screen.show();
						}
						if($('.link', links).size() > 10){
							$('.link:last-child', links).remove();
						}
						link.css('background', actColor).slideDown('slow');
						setTimeout(function(){
							link.animate({
								backgroundColor: '#fff'
							}, colorAnimTime);
						}, colorTimeout);
					}
				}else{
					$.getJSON(
						'?p='+curPage,
						function(data){
							var html = '';
							$.each(data.links, function(i){
								html +=  makeLink(this['code'], this['url'])
							});
							$(links).html(html);
						}
					);
				}
				setPage(curPage, pages.previous, pages.next, pages.last);
			}		
			
			//Обработчики событий
			//переход на другую страницу
			$('a', paginator).click(function(e){
				if (setBusy()) {
					$.getJSON($(this).attr('href'), function(data){
						var html = '';
						$.each(data.links, function(i){
							html += makeLink(this['code'], this['url'])
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
		
		//Форма для сокращения ссылок
		$('#main-input').submit(function(e){
			var isError = $(this).is('.error');
			if(!isError & !checkBusy()){
				//Проверка ссылки
				var url = $('#url', $(this));
				url.trigger('blur');//снимаем фокус
				if (url.val() == '') {
					url.val(MES['Require url']);
					isError = true;
				}else if(url.val() == MES['Wrong url'] || url.val() == MES['Require url'] || url.val() == MES['Alredy Qlink']){
					isError = true;					
				}else if(!isUrl(url.val()) && !isUrl('http://'+url.val())){
					url.data('lastval', url.val());
					url.val(MES['Wrong url']);
					isError = true;
				}else if(isQlink(url.val())){
					url.data('lastval', url.val());
					url.val(MES['Alredy Qlink']);
					isError = true;
				}
				if(isError){
					url.addClass('wrong');
					return false;
				}
				if (setBusy()) {
					//отправляем ссылку
					$.ajax({
						url: $(this).attr('action'),
						type: $(this).attr('method'),
						data: {
							url: url.val(),
							csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
							p: links.curPage
						},
						dataType: 'json',
						success: function(data){
							if (data['error']) {
								url.addClass('wrong');
								if (url.val() != MES['Wrong url']) {
									url.data('lastval', url.val());
								}
								url.val(data['error']['url']);
								isError = true;
							} else {
								links.addLink({
									url: data.link.url,
									code: data.link.code,
									info: data.link.code + '.info'
								}, data.pages);
							}
							setNotBusy();
						}
					});
				}
			}
			return false;
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		//Поле для ссылки
		$('#url').focus(function(e){
			var val = $(this).val();
			if(val == MES['Require url']){
				$(this).val('');
			}else if(val == MES['Wrong url']){
				$(this).val($(this).data('lastval'));
			}else if(val == MES['Alredy Qlink']){
				$(this).val($(this).data('lastval'));
			}
			$(this).removeClass('wrong');
		});
		
		/*-------------------------------------------------------------------------------------------*/
		
		$('#url').keypress(function(e){
			var val = $(this).val();
			if(val == MES['Require url']){
				$(this).val('');
			}else if(val == MES['Wrong url']){
				$(this).val($(this).data('lastval'));
			}
			$(this).removeClass('wrong');
		});
	});
})(jQuery);
