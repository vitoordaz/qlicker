var HOST = 'qliker.ru/'
/**
 * isUrl -- функция для валидации ссылок
 * @param {String} url -- ссылка которую нужно проверить
 * @return {Boolean} -- true -- ссылка, false -- не ссылка
 */
function isUrl(url){
	return (/(https?:\/\/)?(www\.)?(([a-z\-\.]*\.[a-z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(:[0-9]*)?))(\/[\w\d\-\_\.=\+\%\&\#\!\:\@]*)*(\?[\w\d\-\_\.=\+\%\&\#\!\:\@]*)?/i).test(url);
}

/**
 * isThereUrl -- функция определяет есть ли в тексте ссылки
 * @param {String} text -- текст который нужно проверить
 * @return {Boolean} -- true -- есть ссылки, false -- не ссылок
 */
function isThereUrl(text){
	return text.search(/(https?:\/\/)?(www\.)?(([a-z\-\.]*\.[a-z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(:[0-9]*)?))(\/[\w\d\-\_\.=\+\%\&\#\!\:\@]*)*(\?[\w\d\-\_\.=\+\%\&\#\!\:\@]*)?/i) != -1;
}

/**
 * isQlink -- функция для проверки ссылки на qlink
 * @param {String} url -- ссылка, которую нужно проверить
 * @return {Boolean} -- true -- не qlink, false -- qlink
 */
function isQlink(url){
	return /^(http:\/\/)?(www.)?qliker.ru\/[a-z0-9]{1,6}$/i.test(url);
}

/**
 * isEmail -- функция для валидации email
 * @param {String} email -- строка которую нужно проверить
 * @return {Boolean} -- true -- email, false -- не email
 */
function isEmail(email){
	return /^([a-z0-9_\-]+\.)*[a-z0-9_\-]+@([a-z0-9][a-z0-9\-]*[a-z0-9]\.)+[a-z]{2,4}$/i.test(email);
}

/**
 * isSlug -- функция для валидации slug
 * @param {String} slug -- строка которую нужно проверить
 * @return {Boolean} -- true -- slug, false -- не slug
 */
function isSlug(slug){
	return /^[a-z0-9_\-]+$/i.test(slug);
}

$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

/**
 * setBusy -- глобальная функция для установки блокировки
 */
(function($){
	$(function(){
		if (!$('#loading-status').length){
			$('<div id="loading-status">' + MES['Loading...'] + '</div>').appendTo('body');
		}
	})
})(jQuery);
var isBusy = false;
function setBusy(){
	if (!isBusy) {
		$('#loading-status').fadeIn();
		isBusy = true;
		return true;
	}
	return false;
}
function checkBusy(){
	return isBusy;
}
function setNotBusy(){
	$('#loading-status').fadeOut();
	isBusy = false;
}
