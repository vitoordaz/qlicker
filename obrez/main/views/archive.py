#-*- coding: utf-8 -*-
'''
Created on 22.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from main.models import Links

@login_required    
def archive(request):
    ''' Заархивированные ссылки пользователя '''
    try:
        page = int(request.GET.get('p', '1'))
    except ValueError:
        page = 1
    p = Paginator(Links.objects.archived(request.user), 10)
    try:
        links = p.page(page)
    except (EmptyPage, InvalidPage):
        links = p.page(p.num_pages)
    if request.is_ajax():
        c = {}
        c['links'] = [{'url': link.long, 
                       'code': link.code, 
                       'title': link.title, 
                       'date': link.created_at.isoformat(),
                       'favicon': link.favicon,
                       'qlink': link.qlink,
                       'counter': link.counter} for link in links.object_list]
        c['pages'] = {'previous': links.previous_page_number(),
                      'current': links.number,
                      'next': links.next_page_number(),
                      'last': links.paginator.num_pages}
        return HttpResponse(json.dumps(c), mimetype='application/json')
    return render_to_response('archive.html', {'links': links},
                              context_instance=RequestContext(request))
    
@csrf_protect
@login_required
def archivate(request, code):
    ''' Представление для архивирования ссылки '''
    if request.is_ajax():
        try:
            link = Links.objects.for_user(request.user).get(code=code)
            link.archive()
            link.save()
            return HttpResponse('archived')
        except:
            return HttpResponse('not archived')
    return HttpResponseRedirect(reverse('index'))

@csrf_protect
@login_required
def recover(request, code):
    ''' Представление для разархивирования '''
    if request.is_ajax():
        try:
            link = Links.objects.archived(request.user).get(code=code)
            link.recover()
            link.save()
            return HttpResponse('recovered')
        except:
            return HttpResponse('not archived')
    return HttpResponseRedirect(reverse('archive'))