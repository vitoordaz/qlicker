/* jshint strict: true, browser: true */
/* global define */

define([
  'Backbone',
  'underscore',
  'model/link_stat'
], function(Backbone, _, LinkStat) {
  'use strict';

  return Backbone.View.extend({
    initialize: function() {
      var path = location.pathname;
      var linkId = path.match(/^\/([a-zA-Z0-9]+).info$/)[1];
      if (_.isEmpty(linkId)) {
        return;
      }
      this.model = new LinkStat({id: linkId});
      this.listenTo(this.model, 'sync', this.render);
      this.model.fetch();
    },
    render: function() {
      return this;
    }
  });
});