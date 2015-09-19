#-*- coding: utf-8 -*-
'''
Created on 22.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import json, os

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

from main.models import Links
from main.forms import addLinkForm, addLinkFormAuthenticated

from ouser.forms import LoginForm

def index(request):
    '''
    Главная страница. Основания функция добавление ссылок.
    '''
    if request.user.is_anonymous():
        return index_anonymous(request)
    else:
        return index_authenticated(request)

@login_required
def index_authenticated(request):
    '''
    Главная страница для авторизованных пользователей.
    '''
    data = {}
    try:
        page = int(request.GET.get('p', '1'))
    except ValueError:
        page = 1
    if request.method == 'POST':
        if request.POST.get('share', None):
            operation = 'share'
        elif request.POST.get('short', None):
            operation = 'short'
        form = addLinkFormAuthenticated(operation, request.POST)
        if form.is_valid():
            result = form.save(request.user)
            data.update(result)
        elif request.is_ajax():
            return HttpResponse(json.dumps({'error': form.errors}), 
                                mimetype=r'application/json')
    else:
        form = addLinkFormAuthenticated()
    p = Paginator(Links.objects.for_user(request.user), 10)
    try:
        links = p.page(page)
    except (EmptyPage, InvalidPage):
        links = p.page(p.num_pages)
    if request.is_ajax():
        data['links'] = [{'url': link.long, 
                          'code': link.code, 
                          'title': link.title, 
                          'date': link.created_at.isoformat(), 
                          'favicon': link.favicon,
                          'qlink': link.qlink,
                          'counter': link.counter} for link in links.object_list]
        data['pages'] = {'previous': links.previous_page_number(),
                         'current': links.number,
                         'next': links.next_page_number(),
                         'last': links.paginator.num_pages}
        return HttpResponse(json.dumps(data), mimetype=r'application/json')
    c = {'form': form, 'links': links, 
         'services': request.user.services, 
         'active_services': request.user.active_services}
    return render_to_response('index_authenticated.html', c,
                              context_instance=RequestContext(request))

def index_anonymous(request):
    '''
    Главная страница для не авторизованных пользователей.
    '''
    if request.method == 'POST':
        form = addLinkForm(request.POST)
        if form.is_valid():
            l = form.save()
            t = request.session.get('links', [])
            if l not in t:
                t.insert(0, l)
                request.session['links'] = t
        elif request.is_ajax(): # возвращаем ошибки формы для js
            return HttpResponse(json.dumps({'error': form.errors}),
                                mimetype=r'application/json')
    else:
        form = addLinkForm()
    p = Paginator(request.session.get('links', []), 10)
    try:
        page = int(request.GET.get('p', '1'))
    except ValueError:
        page = 1
    try:
        links = p.page(page)
    except (EmptyPage, InvalidPage):
        links = p.page(p.num_pages)
        
    if request.is_ajax():
        data = {}
        if request.method == 'POST':
            data['link'] = {'url': l.long, 'code': l.code}
        else:
            data['links'] = [{'url': link.long, 'code': link.code} for link in links.object_list]
        data['pages'] = {'previous': links.previous_page_number(),
                         'current': links.number,
                         'next': links.next_page_number(),
                         'last': links.paginator.num_pages}
        return HttpResponse(json.dumps(data), mimetype=r'application/json')
    
    return render_to_response('index_anonymous.html', {'form': form, 'auth_form': LoginForm(), 'links': links},
                              context_instance=RequestContext(request))

@csrf_protect
@login_required
def edit_title(request, code):
    ''' Предстваление для редактирования заголовка ссылки '''
    if request.method == 'POST' and request.is_ajax():
        title = request.POST.get('title', None)
        if title:
            try:
                link = Links.objects.for_user(request.user).get(code=code)
                link.set_title(title)
                link.save()
                return HttpResponse('edited')
            except:
                pass
        return HttpResponse('not edited')
    return HttpResponseRedirect(reverse('index'))

def qrcode(request, code):
    '''
    Представление для показа QR кода.
    '''
    filename = os.path.join(settings.QRCODE_DIR, "%s.qr" % code)
    if os.path.exists(filename):
        f = open(filename)
        return HttpResponse(f.read(), content_type='image/png')