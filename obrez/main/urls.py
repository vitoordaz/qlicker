#-*- coding: utf-8 -*-
'''
Created on 04.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from django.conf import settings
from django.conf.urls.defaults import url, include, patterns
from django.views.generic.simple import direct_to_template

from obrez.ouser import urls
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^b/faq/$', direct_to_template, {'template': 'help.html'}, name='help'),
    url(r'^b/terms/$', direct_to_template, {'template': 'terms.html'}, name='terms'),
    url(r'^a/archive/$', views.archive, name='archive'),
    url(r'^a/archivate/(?P<code>[0-9a-zA-Z]+)$', views.archivate, name='archivate'),
    url(r'^a/archive/recover/(?P<code>[0-9a-zA-Z]+)$', views.recover, name='recover'),
    url(r'^a/edit/(?P<code>[0-9a-zA-Z]+)$', views.edit_title, name='edit_title'),
    url(r'^a/', include(urls)),
)

urlpatterns += patterns('',
    url(r'^(?P<code>[0-9a-zA-Z]+).qr$', views.qrcode, name='qrcode'),
)
    
urlpatterns += patterns('',
    url(r'^(?P<code>[0-9a-zA-Z]+).info$', views.info, name='info'),
    url(r'^info/(?P<type>(clicks|domains|countries|referrer))/(?P<interval>(total|days|hourly))/$', views.info_clicks, name='info_clicks'),
)

urlpatterns += patterns('',
    url(r'^(?P<code>[0-9a-zA-Z]+)$', views.redirect, name='redirect'),
)