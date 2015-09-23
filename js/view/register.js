/* jshint strict: true, browser: true */
/* global define */

define([
  'jquery',
  'Backbone',
  'underscore.string',
  'utils'
], function($, Backbone, s, utils) {
  'use strict';
  return Backbone.View.extend({
    events: {
      submit: 'submit',
      'focus input': 'hideError'
    },
    submit: function(e) {
      var username = this.$('#id_username');
      var email = this.$('#id_email');
      var password1 = this.$('#id_password1');
      var password2 = this.$('#id_password2');
      var isValid = true;

      // Validate username.
      if (s.trim(username.val()) === '') {
        this.showError(username, 'Username required');
        username.addClass('invalid');
        isValid = false;
      } else if (s.trim(username.val()).length < 4) {
        this.showError(username, 'Username must be more then 4 symbols');
        username.addClass('invalid');
        isValid = true;
      } else if (!utils.isSlug(s.trim(username.val()))) {
        this.showError(username, 'Invalid username');
        username.addClass('invalid');
        isValid = true;
      }

      // Validate email.
      if (s.trim(email.val()) === '') {
        this.showError(email, 'Email required');
        email.addClass('invalid');
        isValid = false;
      } else if (!utils.isEmail(s.trim(email.val()))) {
        this.showError(email, 'Invalid email');
        email.addClass('invalid');
        isValid = false;
      }

      // Validate password.
      if (s.trim(password1.val()) === '') {
        this.showError(password1, 'Require password');
        password1.addClass('invalid');
        isValid = false;
      }
      if (s.trim(password2.val()) === '') {
        this.showError(password2, 'Require password confirm');
        password2.addClass('invalid');
        isValid = false;
      }
      if (s.trim(password1.val()) !== s.trim(password2.val())) {
        this.showError(password2, 'Password and confirm are not same');
        password1.addClass('invalid');
        password2.addClass('invalid');
        isValid = false;
      } else if (s.trim(password1.val()).length != 0 &&
                 s.trim(password1.val()).length < 6) {
        this.showError(password2, 'Password must be more then 6 symbols');
        password1.addClass('invalid');
        password2.addClass('invalid');
        isValid = false;
      }

      if (!isValid) {
        e.preventDefault();
      }
    },
    showError: function(el, errorMessage) {
      if (el.next('.error').length) {
        el.next('.error').text(errorMessage).show();
      } else {
        $('<div class="error">' + errorMessage + '</div>').insertAfter(el);
      }
    },
    hideError: function(el) {
      this.$(el.target).removeClass('invalid')
      this.$(el.target).next('.error').hide().text('');
    },
  });
});