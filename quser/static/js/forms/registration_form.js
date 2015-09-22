(function($){
	$(function(){
		function showError(el, error){
			if(el.next('.error').length){
				el.next('.error').text(error).show();
			}else{
				$('<div class="error">' + error + '</div>').insertAfter(el);
			}
		}
		
		var formValid = false;
		
		//Форма для регистрации
		$('#reg-form').submit(function(e){
			var login = $('#id_username', $(this));
			var email = $('#id_email', $(this));
			var password1 = $('#id_password1', $(this));
			var password2 = $('#id_password2', $(this));
			
			var ajaxValidateStack = [];
			
			var isError = false;
			
			if(formValid){
				return true;
			}
			
			if(login.val() == ''){
				showError(login, MES['Require login']);
				login.addClass('wrong');
				isError = true;
			}else if(!isSlug(login.val())){
				showError(login, MES['Invalid login']);
				login.addClass('wrong');
				isError = true;
			}else if(login.val().length < 4){
				showError(login, MES['Login must be more then 4 symbols']);
				login.addClass('wrong');
				isError = true;
			}else{
				ajaxValidateStack.push({el: login,
										url: $(this).attr('action'), 
										type: 'GET',
										data: {login: login.val()}});
			}
			
			if(email.val() == ''){
				showError(email, MES['Require email']);
				email.addClass('wrong');
				isError = true;
			}else if(!isEmail(email.val())){
				showError(email, MES['Invalid email']);
				email.addClass('wrong');				
				isError = true;
			}else{
				ajaxValidateStack.push({el: email,
										url: $(this).attr('action'), 
										type: 'GET',
										data: {email: email.val()}});
			}
			
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
			
			var ajaxFieldCount = ajaxValidateStack.length;
			if(ajaxFieldCount){
				var field = null;
				while(field = ajaxValidateStack.pop()){
					with(field){
						$.ajax({
							url: url,
							type: type,
							data: data,
							success: function(data){
								ajaxFieldCount--;
								if(ajaxFieldCount == 0 && isError == false){
									formValid = true;
									$('#reg-form').submit();
								}
							},
							error: function(xhr, status, arg){
								el.addClass('wrong');
								showError(el, xhr.responseText)
								isError = true;
							}	
						});
					}
				}
			}
			
			return false;
		});
		
		$('.wrong').live('focus', function(e){
			$(this).removeClass('wrong');
			$(this).next('.error').fadeOut();
		});
		//Пароль и подтверждение
		$('#id_password1.wrong').live('focus', function(e){
			$(this).removeClass('wrong');
			var password2 = $('#id_password2.wrong');
			if(password2.length && 
				(password2.next('.error:visible').text() == MES['Password and confirm are not same'] ||
				password2.next('.error:visible').text() == MES['Password must be more then 6 symbols'])){
				password2.next('.error').fadeOut();
				password2.removeClass('wrong');
			}
		});
		$('#id_password2.wrong').live('focus', function(e){
			if($(this).next('.error:visible').text() == MES['Password and confirm are not same'] ||
				$(this).next('.error:visible').text() == MES['Password must be more then 6 symbols']){
				$('#id_password1.wrong').removeClass('wrong');
			}
			$(this).removeClass('wrong');
			$(this).next('.error').fadeOut();
		});
	});
})(jQuery);