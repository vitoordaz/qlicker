#-*- coding: utf-8 -*-
'''
Created on 22.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import threading
from django.http import HttpResponseRedirect, Http404

from main.models import Links
from main.models import create_redirect

def redirect(request, code):
    ''' Представление для перенаправления. '''
    try:
        link = Links.objects.get(code=code)
        t1 = threading.Thread(target=create_redirect, name='t1', args=[link, request])
        t1.start()
        return HttpResponseRedirect(link.url)
    except Links.DoesNotExist:
        raise Http404