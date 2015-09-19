#-*- coding: utf-8 -*-
'''
Created on 16.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

import time, json, urlparse
from datetime import datetime

from django.db.models import Count
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from main.fun import norm_url
from country import Country
from links import Links
from geoipdb import GeoIPdb

class RedirectsManager(models.Manager):
    '''
    RedirectsManager --- менеджер для работы с переходами по ссылкам.
    '''
    def for_link(self, link):
        ''' Возвращает все переходы для ссылки '''
        return self.filter(link=link)
    
    def stat(self, type, link, timestamp=None, hourly=False):
        ''' Возвращает все количество клики '''
        if type == 'clicks':
            values = ('date', ) if not hourly else ('created_at', )
            count = 'date'
            order = 'date'
        elif type == 'domains':
            values = ('domain', )
            count = 'referrer'
            order = '-clicks'
        elif type == 'countries':
            values = ('country__code', )
            count = 'country'
            order = '-clicks'
        elif type == 'referrer':
            values = ('domain', 'referrer', )
            count = 'referrer'
            order = '-clicks'
        
        if not timestamp:
            return self.for_link(link).values(*values).annotate(clicks=Count(count)).order_by(order)
        return self.for_link(link).exclude(created_at__lt=timestamp).values(*values).annotate(clicks=Count(count)).order_by(order)
    
    def make_referer(self, referer):
        ''' Получение хоста из ссылки. '''
        try:
            vurl = URLValidator(False)
            vurl(referer)
            referer = norm_url(referer)
            pr = urlparse.urlsplit(referer)
            domain = pr.netloc[:60]
            pr = list(pr)
            pr[0] = pr[1] = ''
            path = urlparse.urlunsplit(pr)[:255]
        except ValidationError:
            domain = path = ''
        return referer, domain, path

    def create_redirect(self, link, request):
        ''' Создание перехода. '''
        link.inc_counter()
        link.save()
        
        # referrer
        referer, domain, path = self.make_referer(request.META.get('HTTP_REFERER', ''))
        
        # country
        ip = request.META.get('REMOTE_ADDR', None)
        country = GeoIPdb.objects.get_country(ip)
        
        return self.create(link=link, country=country, referrer=referer, 
                           domain=domain, path=path)

class Redirects(models.Model):
    '''
    Redirects --- класс модели для сбора информации о переходах по укороченным ссылкам.
    '''
    link = models.ForeignKey(Links, verbose_name=_('Ссылка'))
    
    date = models.DateField(_('Дата перехода'), default=datetime.now(), auto_now=True)
    time = models.TimeField(_('Время перехода'), default=datetime.now(), auto_now=True)
    created_at = models.DateTimeField(_('Дата и время создания'), default=datetime.now(), auto_now=True)
    
    country = models.ForeignKey(Country, verbose_name=_('Страна'), null=True)
    
    domain = models.CharField(_('Домен'), max_length=60, blank=True)
    path = models.CharField(_('Путь'), max_length=255, blank=True)
    referrer = models.URLField(_('Источник'), verify_exists=False, blank=True)
    
    #ip = models.IPAddressField(_('IP клиента'), blank=True, null=True)
    #browser = models.CharField(_('Браузер'), max_length=255, null=True)

    objects = RedirectsManager()

    class Meta:
        app_label = 'main'
        verbose_name = 'Переход по ссылке'
        verbose_name_plural = 'Переходы по ссылкам'
        db_table = 'main_redirects'

    def __unicode__(self):
        return u"%s" % self.country
    
    def get_absolute_url(self):
        return reverse('redirect', self.link.code)
    
    @property
    def timestamp(self):
        ''' Возвращает эпох тайм перехода '''
        return time.mktime(self.date.timetuple())
    
class RedirectsClicksJSONEncoder(json.JSONEncoder):
    ''' A custom JSON encoder for Redirects clicks objects '''
    def default(self, obj):
        return obj
    
class RedirectsCountriesJSONEncoder(json.JSONEncoder):
    ''' A custom JSON encoder for Redirects countries objects '''
    def default(self, redirects):
        return [ {'code': redirect['country__code'], 'clicks': redirect['clicks']} for redirect in redirects ]

class RedirectsDomainsJSONEncoder(json.JSONEncoder):
    ''' A custom JSON encoder for Redirects domains objects '''
    def default(self, redirects):
        return [{'domain': redirect['domain'], 'clicks': redirect['clicks']} for redirect in redirects ]
    
class RedirectsReferrerJSONEncoder(json.JSONEncoder):
    ''' A custom JSON encoder for Redirects referrer objects '''
    def default(self, redirects):
        p = {}
        for redirect in redirects:
            if redirect['domain'] not in p:
                p[redirect['domain']] = []
            p[redirect['domain']].append({'referrer': redirect['referrer'], 'clicks': redirect['clicks']})
        return p

def create_redirect(link, request):
    Redirects.objects.create_redirect(link, request)