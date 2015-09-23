/* jshint strict: true, browser: true */
/* global define */

define(function() {
  var HOST = 'qlicker.co';
  return {
    stripTrailingSlash: function(s) {
      if (s.length !== 1 && s[s.length - 1] === '/') {
        return s.substr(0, s.length - 1);
      }
      return s;
    },
    isUrl: function(url) {
      return (/(https?:\/\/)?(www\.)?(([a-z\-\.]*\.[a-z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(:[0-9]*)?))(\/[\w\d\-\_\.=\+\%\&\#\!\:\@]*)*(\?[\w\d\-\_\.=\+\%\&\#\!\:\@]*)?/i).test(url);
    },
    isThereUrl: function(text) {
      return text.search(/(https?:\/\/)?(www\.)?(([a-z\-\.]*\.[a-z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(:[0-9]*)?))(\/[\w\d\-\_\.=\+\%\&\#\!\:\@]*)*(\?[\w\d\-\_\.=\+\%\&\#\!\:\@]*)?/i) != -1;
    },
    isQlink: function(url) {
      return /^(http:\/\/)?(www.)?qliker.ru\/[a-z0-9]{1,6}$/i.test(url);
    },
    isEmail: function(email) {
      return /^([a-z0-9_\-]+\.)*[a-z0-9_\-]+@([a-z0-9][a-z0-9\-]*[a-z0-9]\.)+[a-z]{2,4}$/i.test(email);
    },
    isSlug: function(slug) {
      return /^[a-z0-9_\-]+$/i.test(slug);
    },
    getCookie: function(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = $.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  };
});