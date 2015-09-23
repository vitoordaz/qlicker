/* jshint strict: true, browser: true */
/* global define */

define(['Backbone'], function(Backbone) {
  'use strict';

  return Backbone.Model.extend({
    idAttribute: 'id',
    url: function() {
      return '/link/' + this.id + '/stat';
    }
  });
});