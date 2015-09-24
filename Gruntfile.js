'use strict';
/* jshint strict: true, node: true */

var path = require('path');

function here() {
  var args = Array.prototype.slice.call(arguments, 0);
  args.unshift(__dirname);
  return path.join.apply(path.join, args);
}

module.exports = function(grunt) {
  var pkg = grunt.file.readJSON(here('package.json'));

  grunt.task.loadNpmTasks('grunt-bower-task');
  grunt.task.loadNpmTasks('grunt-contrib-clean');
  grunt.task.loadNpmTasks('grunt-contrib-concat');
  grunt.task.loadNpmTasks('grunt-contrib-cssmin');
  grunt.task.loadNpmTasks('grunt-contrib-less');
  grunt.task.loadNpmTasks('grunt-contrib-requirejs');
  grunt.task.loadNpmTasks('grunt-contrib-watch');

  grunt.initConfig({
    pkg: pkg,
    bower: {
      install: {
        options: {
          targetDir: '',
          verbose: true,
          layout: function(type, component, source) {
            switch (component) {
              case 'backbone':
              case 'd3':
              case 'jquery':
              case 'moment':
              case 'underscore':
              case 'underscore.string':
              case 'requirejs':
                return path.join('js', 'third_party');
            }
            return 'tmp';
          }
        }
      }
    },
    less: {
      main: {
        expand: true,
        cwd: here('static', 'less'),
        src: '**/*.less',
        dest: here('tmp', 'css'),
        ext: '.css'
      }
    },
    concat: {
      css: {
        src: [
          here('tmp', 'css') + '**/*.css'
        ],
        dest: here('tmp', 'css', 'main.css')
      },
      js: {
        src: [
          here('js', 'third_party', 'require.js'),
          here('tmp', 'js', 'main.js')
        ],
        dest: here('static', 'js', 'main.min.js')
      }
    },
    cssmin: {
      main: {
        files: {
          'static/css/main.min.css': 'tmp/css/main.css'
        }
      }
    },
    requirejs: {
      main: {
        options: {
          baseUrl: 'js',
          optimize: 'none',
          name: 'main',
          out: 'tmp/js/main.js',
          paths: {
            Backbone: here('js', 'third_party', 'backbone'),
            d3: here('js', 'third_party', 'd3'),
            jquery: here('js', 'third_party', 'jquery'),
            moment: here('js', 'third_party', 'moment'),
            underscore: here('js', 'third_party', 'underscore'),
            'underscore.string': here('js', 'third_party', 'underscore.string')
          }
        }
      }
    },
    clean: {
      'tmp-js': {
        force: true,
        src: [here('tmp', 'js')]
      },
      'tmp-css': {
        force: true,
        src: [here('tmp', 'css')]
      }
    },
    watch: {
      css: {
        files: ['static/less/**/*.less'],
        tasks: ['css']
      },
      js: {
        files: ['js/**/*.js'],
        tasks: ['js']
      }
    },
  });

  grunt.registerTask('js', [
    'clean:tmp-js',
    'bower',
    'requirejs',
    'concat:js'
  ]);

  grunt.registerTask('css', [
    'clean:tmp-css',
    'less',
    'concat:css',
    'cssmin'
  ]);

  grunt.registerTask('default', [
    'css',
    'js'
  ]);
};