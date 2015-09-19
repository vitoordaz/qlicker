(function($){
	$(function(){
		//Форма авторизации
		$('#login-form').submit(function(e){
			var login = $('#id_username', $(this));
			var password = $('#id_password', $(this));
			var error = $('.error', $(this));
			var isError = false;
			
			if(login.val() == '' && password.val() == ''){
				error.html(MES['Require login and password']).show();
				login.addClass('wrong');
				password.addClass('wrong');
				isError = true;
			}else if(login.val() == ''){
				error.html(MES['Require login']).show();	
				login.addClass('wrong');		
				isError = true;
			}else if(password.val() == ''){
				error.html(MES['Require password']).show();
				password.addClass('wrong');
				isError = true;
			}
			return !isError;
		});
		$('#id_username, #id_password').focus(function(e){
			$(this).removeClass('wrong');
			$('.error', '#login-form').fadeOut();
		});
	});
})(jQuery);