#-*- coding: utf-8 -*-
'''
Created on 14.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import json
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views

import oauthfacebook, oauthtwitter
from forms import RegistrationForm, LoginForm, ChagePasswordForm, LoadAvatarForm
from models import RegistrationProfile, OUser, Facebook, Twitter, ServiceJSONEncoder

def registration(request):
    ''' Представление для регистрации '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.is_ajax():
        if request.method == 'GET':
            if 'login' in request.GET:
                try:
                    user = OUser.objects.get(username=request.GET['login'])
                    return HttpResponse(_('Пользователь с таким логином уже существует'), status=400)
                except OUser.DoesNotExist:
                    return HttpResponse()
            if 'email' in request.GET:
                try:
                    user = OUser.objects.get(email=request.GET['email'])
                    return HttpResponse(_('Такой адрес электронной почты уже используется'), status=400)
                except OUser.DoesNotExist:
                        return HttpResponse()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.save():#регистрация прошла успешно
                request.session['registration_complete'] = True
                return HttpResponseRedirect(reverse('registration_complete'))
            request.session['registration_fail'] = True
            return HttpResponseRedirect(reverse('registration_error'))#регистрация прошла с ошибками
    else:
        form = RegistrationForm()
    return render_to_response('registration/registration.html', {'form': form},
                              context_instance=RequestContext(request))

def registration_complete(request):
    ''' Успешное завершение регистрации. '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.session.get('registration_complete', None):
        return HttpResponseRedirect(reverse('registration'))
    del request.session['registration_complete']
    return render_to_response('registration/registration_complete.html', {},
                              context_instance=RequestContext(request))

def registration_error(request):
    ''' В ходе регистрации произошла ошибка. '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.session.get('registration_fail', None):
        return HttpResponseRedirect(reverse('registration'))
    del request.session['registration_fail']
    return render_to_response('registration/registration_fail.html', {},
                              context_instance=RequestContext(request))

def activation(request, activation_key):
    ''' Активация пользователя. '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not RegistrationProfile.objects.activate_user(activation_key):
        return render_to_response('registration/activation_fail.html', {},
                                  context_instance=RequestContext(request))
    return render_to_response('registration/activation.html', {},
                              context_instance=RequestContext(request))

def activation_abort(request, activation_key):
    ''' Отмена регистрации пользователя. '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not RegistrationProfile.objects.abort_activation(activation_key):
        return render_to_response('registration/activation_abort_fail.html', {},
                                  context_instance=RequestContext(request))
    return render_to_response('registration/activation_abort.html', {},
                              context_instance=RequestContext(request))

def login(request):
    ''' Представление для авторизации пользователей в системе. '''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return views.login(request, authentication_form = LoginForm,
                       template_name = 'registration/login.html')

def logout(request, next_page):
    ''' Представление для деавторизации пользователей в системе. '''
    if request.user.is_authenticated():
        return views.logout(request, next_page=next_page)
    return HttpResponseRedirect(next_page)

@login_required
def facebook(request):
    ''' Получает access token и сохраняет его в БД '''
    error = request.GET.get('error', None)
    code = request.GET.get('code', None)
    if error:
        return HttpResponseRedirect(reverse('profile'))# TODO: показывать ошибку
    elif code:
        facebook = oauthfacebook.OAuthApi(client_id=settings.FB_CLIENT_ID, client_secret=settings.FB_CLIENT_SECRET, code=code)
        access_token = facebook.getAccessToken(settings.FB_ACCESS_TOKEN_URI)
        fb_user = facebook.getUser()
        fb, created = Facebook.objects.get_or_create(ouser=request.user)
        fb.active = True
        fb.access_token = access_token
        fb.screen_name = fb_user['name']
        fb.user_id = fb_user['id']
        fb.save()
        return HttpResponseRedirect(reverse('profile'))
    facebook = oauthfacebook.OAuthApi(client_id=settings.FB_CLIENT_ID)
    url = facebook.getAuthorizationURL(settings.FB_ACCESS_TOKEN_URI, settings.FB_PERMISSIONS)
    if request.is_ajax():
        return HttpResponse(url)
    return HttpResponseRedirect(url)

@login_required
def twitter_get_auth_link(request):
    ''' Возвращает url для авторизации в twitter '''
    twitter = oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    temp_credentials = twitter.getRequestToken()
    url = twitter.getAuthorizationURL(temp_credentials)
    if request.is_ajax():
        return HttpResponse(url)
    return HttpResponseRedirect(url)

@login_required
def twitter_make_access_token(request):
    ''' Получает access token и сохраняет его в БД '''
    oauth_verifier = request.GET.get('oauth_verifier', None)
    oauth_token = request.GET.get('oauth_token', None)

    if oauth_verifier and oauth_token:
        twitter = oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        temp_credentials = twitter.getRequestToken()
        temp_credentials['oauth_token'] = oauth_token
        access_token = twitter.getAccessToken(temp_credentials, oauth_verifier)
        try:
            tw_data = Twitter.objects.get(ouser=request.user) # обновляем данные пользователя
        except:
            tw_data = Twitter(ouser=request.user)
        tw_data.active = True
        tw_data.screen_name = access_token['screen_name']
        tw_data.oauth_token = access_token['oauth_token']
        tw_data.oauth_token_secret = access_token['oauth_token_secret']
        tw_data.save()
        return HttpResponseRedirect(reverse('profile'))
    raise Http404() # TODO: в ходе операции произошла ошибка

@csrf_protect
@login_required
def service_remove(request, service):
    ''' Удаление сервиса '''
    if service == 'twitter':
        model = Twitter
    elif service == 'facebook':
        model = Facebook
    else:
        raise Http404
    try:
        service = model.objects.get(ouser=request.user)
        service.delete()
        if request.is_ajax():
            return HttpResponse('success')
        return HttpResponseRedirect(reverse('profile'))
    except model.DoesNotExist:
        raise Http404

@csrf_protect
@login_required
def service_toggle(request, service):
    ''' Отключение и включение сервиса '''
    is_index = request.GET.get('index', None)
    if service == 'twitter':
        model = Twitter
    elif service == 'facebook':
        model = Facebook
    else:
        raise Http404
    try:
        service = model.objects.get(ouser=request.user)
        service.active = not service.active
        service.save()
        if request.is_ajax():
            if is_index and service.active:
                return HttpResponse(json.dumps(service, cls=ServiceJSONEncoder), 
                                    mimetype='application/json')
            return HttpResponse(json.dumps(service.active),
                                mimetype=r'application/json')
        if is_index:
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('profile'))
    except model.DoesNotExist:
        raise Http404

@login_required
def profile(request, action=''):
    ''' Профайл пользователя. '''
    c = {}
    if request.method == 'POST':
        if action == 'password_change':
            c['ch_pswd_form'] = ChagePasswordForm(request.user, request.POST)
        else:
            c['ch_pswd_form'] = ChagePasswordForm(request.user)
        if not request.user.avatar:
            if action == 'avatar_load':
                c['avatar_form'] = LoadAvatarForm(request.user, request.POST, request.FILES)
            else:
                c['avatar_form'] = LoadAvatarForm(request.user)
    else:
        c['services'] = request.user.services
        c['ch_pswd_form'] = ChagePasswordForm(request.user)
        if not request.user.avatar:
            c['avatar_form'] = LoadAvatarForm(request.user)
    return render_to_response('registration/profile.html', c, context_instance=RequestContext(request))

@login_required
def password_change(request):
    ''' Смена пароля. '''
    if request.method == 'POST':
        ch_pswd_form = ChagePasswordForm(request.user, request.POST)
        if ch_pswd_form.is_valid():
            ch_pswd_form.save()
            if request.is_ajax():
                return HttpResponse()
            return HttpResponseRedirect(reverse('profile'))
        if request.is_ajax():
            return HttpResponse(json.dumps({'error': ch_pswd_form.errors}))
        return profile(request, 'password_change')
    return HttpResponseRedirect(reverse('profile'))

@csrf_protect
def password_reset(request, template_name, password_reset_form):
    ''' Представление ввода email для смены пароля. '''
    if request.is_ajax():
        if request.method == 'GET':
            if 'email' in request.GET:
                user = OUser.objects.filter(email__iexact=request.GET['email']).count()
                if user == 0:
                    return HttpResponse(_("Пользователь с таким адресом электронной почты не зарегистрирован"), status=400)
                return HttpResponse('')
    return views.password_reset(request,
                                template_name=template_name,
                                password_reset_form=password_reset_form)

@login_required
@csrf_protect
def avatar_reset(request):
    ''' Сброс аватара, на аватар поумолчанию или из гравотара. '''
    if request.user.avatar:
        request.user.avatar.delete()
    if request.is_ajax():
        return render_to_response('forms/avatar_form.html', {'avatar_form': LoadAvatarForm(request.user)},
                                  context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('profile'))

@login_required
def avatar_load(request):
    ''' Загрузка аватара. '''
    if request.method == 'POST':
        avatar_form = LoadAvatarForm(request.user, request.POST, request.FILES)
        if avatar_form.is_valid():
            avatar_form.save()
            return HttpResponseRedirect(reverse('profile'))
        return profile(request, 'avatar_load')
    return HttpResponseRedirect(reverse('profile'))