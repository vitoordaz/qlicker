(function($){
	$(function(){
		//Сброс аватара
		$('#reset-avatar').live('click', function(e){
			$.ajax({
				url: $(this).attr('href'),
				type: 'GET',
				dataType: 'text',
				success: function(data){
					$('#manage-avatar').html(data);
				}
			});
			return false;
		});
		
		//Отправка изображения
		function showError(el, error){
			if(el.parent().find('.error').length){
				el.find('.error').text(error).show();
			}else{
				$('<div class="error">' + error + '</div>').insertAfter(el.parent().next());
			}
		}
		
		$('#avatar_form').live('submit', function(e){
			var avatar = $('#id_avatar');
			isError = false;
			
			if(avatar.val() == ''){
				showError(avatar, MES['Require image']);
				isError = true;
			}
			
			return !isError;
		});
		
		$('#id_avatar').live('change', function(e){
			$('.error', '#avatar_form').hide();
		});
	});
})(jQuery);