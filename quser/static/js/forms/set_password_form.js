(function($){
	$(function(){
		function showError(el, error){
			if(el.next('.error').length){
				el.next('.error').text(error).show();
			}else{
				$('<div class="error">' + error + '</div>').insertAfter(el);
			}
		}
		
		//Форма для смены пароля
		$('#set-pswd-form').submit(function(e){
			var password1 = $('#id_new_password1', $(this));
			var password2 = $('#id_new_password2', $(this));
			
			var isError = false;
			
			if(password1.val() == ''){
				showError(password1, MES['Require password']);
				password1.addClass('wrong');
				isError = true;
			}
			
			if(password2.val() == ''){
				showError(password2, MES['Require password confirm']);
				password2.addClass('wrong');
				isError = true;
			}
			
			if(password1.val() != password2.val()){
				showError(password2, MES['Password and confirm are not same']);
				password1.addClass('wrong');
				password2.addClass('wrong');
				isError = true;
			}else if(password1.val().length != 0 && password1.val().length < 6){
				showError(password2, MES['Password must be more then 6 symbols']);
				password1.addClass('wrong');
				password2.addClass('wrong');
				isError = true;
			}
			
			return !isError;
		});
		
		$('.wrong').live('focus', function(e){
			$(this).removeClass('wrong');
			$(this).next('.error').fadeOut();
		});
		//Пароль и подтверждение
		$('#id_new_password1.wrong').live('focus', function(e){
			$(this).removeClass('wrong');
			var password2 = $('#id_new_password2.wrong');
			if(password2.length && 
				(password2.next('.error:visible').text() == MES['Password and confirm are not same'] ||
				password2.next('.error:visible').text() == MES['Password must be more then 6 symbols'])){
				password2.next('.error').fadeOut();
				password2.removeClass('wrong');
			}
		});
		$('#id_new_password2.wrong').live('focus', function(e){
			if($(this).next('.error:visible').text() == MES['Password and confirm are not same'] ||
				$(this).next('.error:visible').text() == MES['Password must be more then 6 symbols']){
				$('#id_new_password1.wrong').removeClass('wrong');
			}
			$(this).removeClass('wrong');
			$(this).next('.error').fadeOut();
		});
	});
})(jQuery);