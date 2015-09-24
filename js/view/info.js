/* jshint strict: true, browser: true */
/* global define */

define([
  'Backbone',
  'underscore',
  'moment',
  'd3',
  'model/link_stat'
], function(Backbone, _, moment, d3, LinkStat) {
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
      if (_.isEmpty(this.model.get('redirects'))) {
        this.$('.redirects').hide();
      } else {
        this.$('.redirects').show();
        this.renderRedirectsChart();

        this.$('.countries').show();
        this.renderCountriesChart();

        this.$('.referrer').show();
        this.renderReferrerChart();
      }
      return this;
    },
    renderRedirectsChart: function() {
      var data = this.model.get('redirects');
      var $chart = this.$('.redirects-chart');
      var margin = {top: 20, right: 20, bottom: 20, left: 25};
      var width = $chart.width() - margin.right - margin.left;
      var height = $chart.height() - margin.top - margin.bottom;
      var barWidth = Math.min(width / data.length, 10);
      var widthOffset = 0;
      if (barWidth * data.length < width) {
        widthOffset = (width - barWidth * data.length) / 2;
      }

      var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
      x.domain(data.map(function(d) {
        return moment(new Date(d.date)).format('L');
      }));
      var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom');

      var y = d3.scale.linear().range([height, 0]);
      var maxRedirects = d3.max(data, function(d) {
        return d.redirects;
      });
      y.domain([0, maxRedirects]);
      var yAxis = d3.svg.axis()
        .scale(y)
        .orient('left')
        .ticks(Math.min(10, maxRedirects));

      var chart = d3.select('.redirects-chart')
        .attr('width', width + margin.right + margin.left)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
          .attr('transform',
                'translate(' + margin.left + ',' + margin.top + ')');

      chart.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

      chart.append('g')
        .attr('class', 'y axis')
        .call(yAxis)
        .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '.71em')
          .style('text-anchor', 'end')
          .text('Redirects');

      chart.selectAll('.bar')
          .data(data)
        .enter().append('rect')
          .attr('class', 'bar')
          .attr('x', function(d) {
            return x(moment(new Date(d.date)).format('L'));
          })
          .attr('width', x.rangeBand())
          .attr('y', function(d) {
            return y(d.redirects);
          })
          .attr('height', function(d) {
            return height - y(d.redirects);
          });
    },
    renderCountriesChart: function() {}
    renderReferrerChart: function() {}
  });
});