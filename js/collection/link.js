/* jshint strict: true */
/* globals define */

define(['Backbone', 'model/link'], function(Backbone, Link) {
  'use strict';

  return Backbone.Collection.extend({
    url: 'link/',
    model: Link,
    parse: function(response) {
      this.total = response.meta.total;
      return response.data;
    },
    comparator: function(i) {
      return -i.get('created_at');
    }
  });
});