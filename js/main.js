/* jshint strict: true, browser: true */

require([
  'Backbone',
  'jquery',
  'utils',
  'app'
], function(Backbone, $, utils, App) {
  $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
    var token = utils.getCookie('csrftoken');
    options.xhrFields = {withCredentials: true};
    if (token) {
      return jqXHR.setRequestHeader('X-CSRFToken', token);
    }
  });

  var APP = new App();
  APP.run();
});