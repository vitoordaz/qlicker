/* jshint strict: true, browser: true */

define([
  'jquery',
  'Backbone',
  './utils',
  'view/add_link',
  'view/login',
  'view/register',
  'view/password_reset'
], function($, Backbone, utils, AddLinkView, LoginView, RegisterView,
            PasswordResetView) {
  'use strict';
  function App() {}

  App.prototype.run = function() {
    var path = utils.stripTrailingSlash(location.pathname);
    var view;
    if (path === '/') {
      view = new AddLinkView({el: $('#add-link-view')});
      view.render();
    } else if (path === '/login') {
      view = new LoginView({el: $('#login-view')});
      view.render();
    } else if (path === '/register') {
      view = new RegisterView({el: $('#register-view')});
      view.render();
    } else if (path === '/password/reset') {
      view = new PasswordResetView({el: $('#password-reset-view')});
      view.render();
    }
  };

  return App;
});