(function($){
    $(function(){

        /**
         * Links -- класс для работы с ссылками
         */
        function Links(){
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
                                    '<div class="param"></div>'+
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
             *                      code -- код ссылки в системе
             *                      counter -- количество переходов
             *                      date -- дата добавления ссылки
             *                      favicon -- favicon страницы ссылки
             *                      qlink -- Qlink
             *                      title -- title страницы ссылки
             *                      url -- номализованная ссылка (http://qliker.ru)
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
							    '<a href="/a/archive/recover/' + link['code'] + '">' + MES['Recover'] + '</a>'+
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
             *                  added -- массив добавленных ссылок
             *                      qlink -- Qlink
             *                      code -- код ссылки
             *                      url -- исходная ссылка
             *                  links -- массив ссылок для данной страницы (curPage)
             *                      code -- код ссылки в системе
             *                      counter -- количество переходов
             *                      date -- дата добавления ссылки
             *                      favicon -- favicon страницы ссылки
             *                      qlink -- Qlink
             *                      title -- title страницы ссылки
             *                      url -- номализованная ссылка (http://qliker.ru)
             *                  pages -- объект содержащий:
             *                      last -- последняя страница
             *                      previous -- предыдущая страница
             *                      current -- текущая страница
             *                      next -- следующая страница
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
                        $.getJSON('.', function(data){
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
                    });
                }
                return false;
            });
        }
        
        var links = new Links();

		$('.param a', '#links-list').live('click', function(e){
			if (setBusy()) {
				var link = $(this);
				$.ajax({
					url: link.attr('href'),
					type: 'post',
					dataType: 'text',
					data: {'csrfmiddlewaretoken': $('input[name]=csrfmiddlewaretoken').val()},
					success: function(data){
						links.removeLink(link.parents('.link.oh', '#links-list').attr('code'));
						setNotBusy();
					}
				});	
			}
			return false;
		});
    });
})(jQuery);