/* jshint strict: true, browser: true */
/* global define */

define(['jquery', 'Backbone', 'underscore.string'], function($, Backbone, s) {
  'use strict';
  return Backbone.View.extend({
    events: {
      submit: 'submit',
      'focus input[type=text]': 'hideError',
      'focus input[type=password]': 'hideError'
    },
    submit: function(e) {
      var username = this.$('input[name=username]');
      var password = this.$('input[name=password]');
      var isValid = true;
      if (s.trim(username.val()) == '' && s.trim(password.val()) == '') {
        this.$('.error').text('Username and password required');
        username.addClass('invalid');
        password.addClass('invalid');
        isValid = false;
      } else if (s.trim(username.val()) === '') {
        this.$('.error').text('Username required');
        username.addClass('invalid');
        isValid = false;
      } else if (s.trim(password.val()) === '') {
        this.$('.error').text('Password required');
        password.addClass('invalid');
        isValid = false;
      }
      if (!isValid) {
        e.preventDefault();
      }
    },
    hideError: function() {
      this.$el.removeClass('invalid');
      this.$('.error').html('');
    },
  });
});