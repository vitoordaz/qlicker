(function($){
    $(function(){
		/**
		 * Clicks statistic
		 */
		$.ajax({
			url: '/info/clicks/total/',
			type: 'GET',
			dataType: 'json',
			data: {'code': code},
			success: function(data){
                var height = 260, 
					width = 940,
					values = [],
					hlabels = [];
				for (var i in data['data']) {
					values.push(data['data'][i].clicks);
					var date = new Date(data['data'][i].timestamp * 1000);
					hlabels.push(date.getDate() + ' ' + MONTH[date.getMonth()] + ' ' + date.getFullYear());
				}
				var total = Math.max.apply(Math, values),
					mh = height / total,
					len = values.length, 
				    html = '',
					fullw = width / len,
					gw = fullw * 0.2,
					barw = fullw - gw,
					left = 0;
                if (total == 0) {
					$('#click-bar').addClass('empty').text(MES['Empty clicks']);
                    return;
                }
				for (var i in values) {
					var h = values[i] ? values[i] * mh : 1;
					html += '<div class="bar" style="width: ' + barw + 'px; height: ' + height + 'px; position: absolute; left: ' + left + 'px;">'+
					            '<div class="top" height="' + (height-h) + '" style="height: ' + height + 'px;"></div>'+
								'<div class="bottom" height="' + h + '" style="height: ' + 0 + 'px;"></div>'+
							'</div>';
					left += barw + gw;
				}
				
				for (var i = 1; i <= total; i *= 10);
				var vlabels = '<div class="vt" style="top: ' + height + 'px;">0</div>',
				    hl = '',
					m = i / 10,
					all = Math.floor(total / m),
					top = 0;
				for (var i = 1; i <= all; ++i ) {
					top = height - i*mh*m;
					vlabels += '<div class="vt" style="top: ' + top + 'px;">' + i*m + '</div>';
					hl += '<div style="top: +' + top + 'px" class="hl"></div>'
				}
				var hlabel = '',
				    hlw = 67;
				if (hlabels.length * hlw > width) {
					var all = Math.floor(width / hlw),
					    sl = Math.floor(hlabels.length / all);
					for (var i = 0; i < all; i++) {
						hlabel += '<div class="ht" style="left: ' + i*hlw + 'px;">' + hlabels[i*sl] + '</div>';
					} 
				} else {
                    var left = 0;
                    for (var i in hlabels) {
                        hlabel += '<div class="ht" style="left: ' + left + 'px;">' + hlabels[i] + '</div>';
						left += barw + gw;
                    }
				}
				html = '<div class="y">' + vlabels + '</div><div class="axes">' + hl + html + '</div>' + '<div class="x">' + hlabel + '</div>';
				$('#click-bar').html(html);
				
				$('.bottom').each(function(i){
					var h = $(this).attr('height');
					if (h != 1) {
						$(this).animate({
							height: h + 'px'
						}, 800);
					}else{
						$(this).css('height', 1);
					}
				});
                $('.top').each(function(i){
					var h = $(this).attr('height');
					if (h != height - 1) {
						$(this).animate({
							height: h + 'px'
						}, 800);
					}else{
						$(this).css('height', height - 1);
					}
				});
			}
		});
		
        /**
         * Countries statistic
         */
        $.ajax({
            url: '/info/countries/total/',
            type: 'GET',
            dataType: 'json',
            data: {'code': code},
            success: function(data){
                var stat = data['data'], res = [], leg = [], html = '', country = '', counter = 0, lcountry = '';
                for (i in stat) {
					res.push(stat[i].clicks);
					country = COUNTRY[stat[i].code];
					lcountry = (country.length > 12) ? country.substr(0, 12) + '...' : country;
					leg.push(lcountry);
					html += '<div class="oh' + ((counter > 8)? ' hidden' : '') + '"><div class="fl"><span>' + (stat[i].code != '??' ? stat[i].code : '&nbsp;') + '</span>' + country + '</div><div class="fr">' + stat[i].clicks + '</div></div>';
					counter++;
                }
                if (counter == 0){
                    return;
                }
                html = '<h3>' + MES['Clicks by countries'] + '</h3><div id="countries-pie"></div><h3>' + MES['Details clicks by countries'] + '</h3><div id="countries-detail">' + html + '</div>';
                if (counter > 8) {
					html += '<div class="more"><a href="javascript:void(0);">' + MES['More'] + '</a></div>';
				}
				$('#countries').html(html);
				
                var r = Raphael('countries-pie');
                var pie = r.g.piechart(450/2+20, 230/2, 200/2, res, {legend: leg, legendpos: 'west', legendothers: MES['Others']});
                pie.hover(function () {
                    this.sector.stop();
                    this.sector.scale(1.05, 1.05, this.cx, this.cy);
                    if (this.label) {
                        this.label[0].stop();
                        this.label[0].scale(1.5);
                        this.label[1].attr({"font-weight": 800});
                    }
                }, function () {
                    this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
                    if (this.label) {
                        this.label[0].animate({scale: 1}, 500, "bounce");
                        this.label[1].attr({"font-weight": 400});
                    }
                });	
            }
        });
		
        /**
         * Domains statistic
         */
        $.ajax({
            url: '/info/domains/total/',
            type: 'GET',
            dataType: 'json',
            data: {'code': code},
            success: function(data){
                var stat = data['data'], res = [], leg = [], html = '', domain = '', counter = 0, ldomain = '';
                for (i in stat) {
					res.push(stat[i].clicks);
				    domain = (stat[i].domain) ? stat[i].domain : MES['Direct'];
					ldomain = (domain.length > 12)? domain.substr(0, 12) + '...' : domain;
                    leg.push(ldomain);
					if (stat[i].domain) {
						html += '<div domain="' + stat[i].domain + '" class="oh' + ((counter > 8) ? ' hidden' : '') + '"><div class="fl"><a class="tree" href="javascript:void(0);">+</a> ' + domain + '</div><div class="fr">' + stat[i].clicks + '</div></div>';
					} else {
						html += '<div domain="' + stat[i].domain + '" class="oh' + ((counter > 8) ? ' hidden' : '') + '"><div class="fl"><a class="tree">&nbsp;&nbsp;</a> ' + domain + '</div><div class="fr">' + stat[i].clicks + '</div></div>';
					}
                    counter++;
				}
				if (counter == 0){
					return;
				}
                html = '<h3>' + MES['Clicks by domains'] + '</h3><div id="domains-pie"></div><h3>' + MES['Details clicks by domains'] + '</h3><div id="domains-detail">' + html + '</div>';
				if (counter > 8) {
					html += '<div class="more"><a href="javascript:void(0);">' + MES['More'] + '</a></div>';
				}
				$('#domains').html(html);
				
                var r = Raphael('domains-pie');
                var pie = r.g.piechart(450/2+20, 230/2, 200/2, res, {legend: leg, legendpos: 'west', legendothers: MES['Others']});
                pie.hover(function () {
                    this.sector.stop();
                    this.sector.scale(1.05, 1.05, this.cx, this.cy);
                    if (this.label) {
                        this.label[0].stop();
                        this.label[0].scale(1.5);
                        this.label[1].attr({"font-weight": 800});
                    }
                }, function () {
                    this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
                    if (this.label) {
                        this.label[0].animate({scale: 1}, 500, "bounce");
                        this.label[1].attr({"font-weight": 400});
                    }
                });
            }
        });
		/**
		 * Refererrs statistic
		 */
		var is_referrers = false;
		$('#domains-detail .tree').live('click', function(e){
			var context = $(this).parent().parent();
			if (!$('.referrers', context.parent()).length && !is_referrers) {
				is_referrers = true;
				$.ajax({
					url: '/info/referrer/total/',
					type: 'GET',
					dataType: 'json',
					data: {
						'code': code
					},
					success: function(data){
						var stat = data['data'];
						for (i in stat) {
							if (i == '') 
								continue;
							var html = '', path = '';
							for (j in stat[i]) {
								path = stat[i][j].referrer.substr(('http://' + i).length).substr(0, 75);
								html += '<div class="oh"><div class="fl"><a href="' + stat[i][j].referrer + '">' + path + '</a></div><div class="fr">' + stat[i][j].clicks + '</div></div>';
							}
							$('<div class="referrers">' + html + '</div>').hide().appendTo('#domains-detail div[domain="' + i + '"]');
						}
						$('.referrers', context).show();
					}
				});
			} else {
				$('.referrers', context).toggle();
			}
		});
		/**
		 * Handlers
		 */
		$('.more a').live('click', function(e){
			var details = $(this).parent().prev();
			$(this).text( $(this).text() == MES['More'] ? MES['Less'] : MES['More'] );
			$('.oh.hidden', details).toggle();
		});
    });
})(jQuery);