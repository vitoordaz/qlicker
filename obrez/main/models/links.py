#-*- coding: utf-8 -*-
'''
Created on 16.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import re, urllib, threading, json
from datetime import datetime

from django.db import models
from django.utils.safestring import mark_for_escaping
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from ouser.models import OUser
from main.fun import encode, QRCodeGen, norm_url, get_link_meta

HOST = re.compile(
    r'^(https?://)?' # http:// or https://
    r'(www\.)?'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?', re.IGNORECASE) # optional port

class LinksManager(models.Manager):
    ''' Менеджер для ссылок '''
    def archived(self, user):
        ''' Все заархивированные ссылки пользователя '''
        return self.filter(inarchive=True).order_by('-updated_at').filter(user=user)
    
    def for_user(self, user):
        ''' Все активные ссылки для заданного пользователя '''
        return self.filter(inarchive=False).order_by('-updated_at').filter(user=user)

class Links(models.Model):
    '''
    Links --- класс модели для хранения ссылок.
    '''
    inarchive = models.BooleanField(verbose_name=_('В архиве'), default=False)
    url = models.URLField(verbose_name=_('Ссылка'))
    code = models.CharField(verbose_name=_('Код'), max_length=10, 
                            null=True, blank=True, editable=False)
    counter = models.IntegerField(verbose_name=_('Переходы'),
                                  default=0, null=True, help_text=_('Количество переходов по ссылке'))
    user = models.ForeignKey(OUser, verbose_name=_('Владелец'),
                             null=True, blank=True, 
                             help_text=_('Пользователь добавивший ссылку'))
    
    created_at = models.DateTimeField(verbose_name=_('Создано'), default=datetime.now(), 
                                      help_text=_('Время добавления ссылки'))
    updated_at = models.DateTimeField(verbose_name=_('Обновлено'), default=datetime.now(), 
                                      help_text=_('Дата и время последнего добавления ссылки'))
    
    title = models.CharField(verbose_name=_('Заголовок страницы'),
                             max_length=150, blank=True, null=True)
    
    objects = LinksManager()
    
    class Meta:
        app_label = 'main'
        verbose_name = u'Ссылка'
        verbose_name_plural = u'Ссылки'
        db_table = 'main_links'
        ordering = ('-updated_at', '-id')

    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            kwargs['url'] = norm_url(kwargs['url'])
        super(Links, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % (self.url)
    
    @property
    def favicon(self):
        return "%sfavicon/%s.png" % (settings.MEDIA_URL, self.code)
    
    @property
    def qlink(self):
        return "%s/%s" % (settings.SITE_URL, self.code)
    
    @property
    def long(self):
        return urllib.unquote(self.url.encode('utf-8'))
    
    def set_title(self, title):
        ''' Изменяет заголовок страницы '''
        self.title = mark_for_escaping(title)
    
    def archive(self):
        self.inarchive = True
        
    def recover(self):
        self.inarchive = False
    
    def updated_now(self):
        ''' Фиксирует обновление ссылки '''
        self.updated_at = datetime.now()
    
    def inc_counter(self):
        ''' Увеличивает количество переходов по ссылке '''
        self.counter += 1
            
    def save(self, **kwargs):
        super(Links, self).save(**kwargs)
        if not self.code:
            self.code = encode(self.id)
            # генерация qr кода
            qr = QRCodeGen(self.code)
            qr.start()
            if self.user:
                get_link_meta(self)
            else:
                m = threading.Thread(target=get_link_meta, name='t1', args=[self])
                m.start()
            super(Links, self).save()

class LinksJSONEncoder(json.JSONEncoder):
    ''' A custom JSON encoder for Links objects '''
    def default(self, link):
        if not isinstance (link, Links):
            print 'You cannot use the JSON custom LinksJSONEncoder for a non-Links object.'
            return
        return {'url': link.url, 'qlink': link.qlink, 'favicon': link.favicon, 
                'title': link.title, 'date': str(link.date), 'counter': link.counter}