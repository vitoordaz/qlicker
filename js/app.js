/* jshint strict: true, browser: true */

define([
  'jquery',
  'Backbone',
  './utils',
  'view/add_link',
  'view/info',
  'view/login',
  'view/register',
  'view/password_reset'
], function($, Backbone, utils, AddLinkView, InfoView, LoginView, RegisterView,
            PasswordResetView) {
  'use strict';
  function App() {}

  App.prototype.run = function() {
    var path = utils.stripTrailingSlash(location.pathname);
    var view;
    if (path === '/') {
      view = new AddLinkView({el: $('#add-link-view')});
    } else if (path === '/login') {
      view = new LoginView({el: $('#login-view')});
    } else if (path === '/register') {
      view = new RegisterView({el: $('#register-view')});
    } else if (path === '/password/reset') {
      view = new PasswordResetView({el: $('#password-reset-view')});
    } else if (/^\/[a-zA-Z0-9]+.info$/.test(path)) {
      view = new InfoView({el: $('#link-info-view')});
    }
    if (view) {
      view.render();
    }
  };

  return App;
});