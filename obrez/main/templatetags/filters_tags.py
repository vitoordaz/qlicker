'''
Created on 18.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

import urllib2

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def unquote(value):
    return urllib2.unquote(value.encode('utf-8'))