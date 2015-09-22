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
		
		//Форма для сброса пароля
		$('#pswd-reset-form').submit(function(e){
			var email = $('#id_email', $(this));
			
			var ajaxValidateStack = [];
			
			var isError = false;
			
			if(formValid){
				return true;
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
									$('#pswd-reset-form').submit();
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
	});
})(jQuery);