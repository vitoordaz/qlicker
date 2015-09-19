#-*- coding: utf-8 -*-
'''
Created on 04.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import re

from django import forms
from django.utils.translation import gettext_lazy as _

from fun import norm_url
from models import Links

URL_PATTERN = re.compile(r'(:?http://|https://)?'
                         r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
                         r'[A-Z]{2,6}\.?/?'
                         r'(?:/?[A-Z0-9-_\.\?=\+\%\&\#\!\:]/?)*', re.IGNORECASE)

QLINK_PATTERN = re.compile(r'^(http://)?(www\.)?qliker.ru/[a-zA-Z0-9]{1,6}$', re.IGNORECASE)

class addLinkForm(forms.Form):
    '''
    addLinkForm --- класс формы для добавления ссылки.
    '''
    url = forms.URLField(required=True,
                         error_messages={'required': _('Укажите ссылку'),
                                         'invalid': _('Укажите правильную ссылку'),
                                         'invalid_link': _('Адресс, на который ссылается ссылка недоступен')})
    
    def clean_url(self):
        url = self.cleaned_data.get('url', None)
        if url:
            url = norm_url(url)
            if re.match(QLINK_PATTERN, url):
                raise forms.ValidationError(_('Уже Qlink'))
            return url
    
    def save(self):
        obj, created = Links.objects.get_or_create(url=self.cleaned_data['url'], user=None)
        return obj

class addLinkFormAuthenticated(forms.Form):
    '''
    addLinkFormAuthenticated --- класс формы для добавления ссылок и отправки сообщений.
    '''
    url = forms.CharField(widget=forms.Textarea(attrs={'cols': 65, 'rows': 3, 'autocomplete': 'off'}),
                          required=False)
    
    class Media:
        css = {'all': ('css/forms/add_link_form_authenticated.css',)}
    
    def __init__(self, operation=None, *args, **kwargs):
        self.operation = operation
        super(addLinkFormAuthenticated, self).__init__(*args, **kwargs)
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        if self.operation == 'short':
            if url == '':
                raise forms.ValidationError(_('Введите ссылку'))
            elif not re.findall(URL_PATTERN, url):
                raise forms.ValidationError(_('Введите правильную ссылку'))
            elif re.match(QLINK_PATTERN, self.cleaned_data['url']):
                raise forms.ValidationError(_('Уже Qlink'))
        elif self.operation == 'share':
            if url == '':
                raise forms.ValidationError(_('Введите сообщение'))            
        return url  
    
    def save(self, user):
        match = URL_PATTERN.finditer(self.cleaned_data['url'])
        msg = self.cleaned_data['url']
        objs = {'added': []}
        for url in match:
            nurl = norm_url(url.group())
            if not QLINK_PATTERN.match(nurl):
                obj, created = Links.objects.get_or_create(url=nurl, user=user)
                obj.recover()
                obj.updated_now()
                obj.save()
                objs['added'].append({'code': obj.code, 'qlink': obj.qlink, 'url': url.group()})
                msg = msg.replace(url.group(), obj.qlink)
        # обновляем статусы в сервисах
        if self.operation == 'share':
            objs['status'] = user.update_status(msg)
        return objs