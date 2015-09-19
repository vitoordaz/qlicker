#-*- coding: utf-8 -*-
'''
Created on 20.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.conf import settings

def site(request):
    '''
    Контекст процессор для определения текущего сайта.
    '''
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    name = site.name
    domain = site.domain if not settings.DEBUG else 'qliker.ru'
    return {'SITE': {'name': name, 'domain': domain}}