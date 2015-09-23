/* jshint strict: true, browser: true */
/* global define */

define([
  'jquery',
  'Backbone',
  'underscore',
  'underscore.string',
  'utils',
  'collection/link',
  'model/link'
], function($, Backbone, _, s, utils, LinkList, Link) {
  'use strict';

  var LinkView = Backbone.View.extend({
    tagName: 'div',
    template: function() {
      return _.template($('#link-template').html());
    },
    render: function() {
      this.$el.html(this.template()(this.model.attributes));
      this.$el.addClass('link');
      return this;
    }
  });

  return Backbone.View.extend({
    events: {
      'submit form': 'submit',
      'focus form input[name=url]': 'hideError'
    },
    initialize: function() {
      this.links = new LinkList();
      this.listenTo(this.links, 'all', this.render.bind(this));
      this.listenTo(this.links, 'add', this.addLink.bind(this));
      this.links.fetch();
    },
    render: function() {
      if (this.links.total > 0) {
        this.$('.links-wrapper').show();
        this.$('.links .items').html('');
        this.links.each(this.addLink, this);
      }
      return this;
    },
    addLink: function(link) {
      var view = new LinkView({model: link});
      this.$('.links .items').append(view.render().el);
    },
    submit: function(e) {
      e.preventDefault();

      var isValid = true;
      var $url = this.$('form input[name=url]');
      var url = s.trim($url.val());

      if (url === '') {
        this.$('form .error').text('URL required').show();
        isValid = false;
      } else if (!utils.isUrl(url) && !utils.isUrl('http://' + url)) {
        this.$('form .error').text('Invalid URL').show();
        isValid = false;
      } else if (utils.isQlink(url)) {
        this.$('form .error').text('Alredy short link').show();
        isValid = false;
      }

      if (!isValid) {
        $url.addClass('invalid');
      } else {
        $url.removeClass('invalid');
        var link = new Link({url: url});
        link.save(null, {
          success: function() {
            $url.val('');
            this.links.fetch();
          }.bind(this)
        });
      }
    },
    hideError: function(e) {
      this.$(e.target).removeClass('invalid');
      this.$('form .error').text('');
    }
  });
});