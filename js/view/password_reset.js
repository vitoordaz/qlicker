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
      var email = this.$('#id_email');
      var isValid = true;

      // Validate email.
      if (s.trim(email.val()) === '') {
        this.showError(email, 'Require email');
        email.addClass('invalid');
        isValid = false;
      } else if (!utils.isEmail(s.trim(email.val()))) {
        this.showError(email, 'Invalid email');
        email.addClass('invalid');
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