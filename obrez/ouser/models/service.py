#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import json, os, hashlib, datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ouser.utils import AvatarLoader

class ServiceManager(models.Manager):
    def for_user(self, user):
        """ Возвращает сервис привязанный к пользователю """
        try:
            return self.filter(active=True).get(ouser=user)
        except self.model.DoesNotExist:
            return None
        
    def active(self):
        ''' Возвращает все активные сервисы '''
        self.filter(active=True)

class ServiceJSONEncoder(json.JSONEncoder):
    ''' A custom JSON encoder for Service objects '''
    def default(self, service):
        if not isinstance (service, Service):
            print 'You cannot use the JSON custom ServiceJSONEncoder for a non-Service object.'
            return
        return {'user_name': service.user_name, 
                'ico': service.ico, 
                'slug': service.slug, 
                'title': service.title, 
                'mesmaxlen': service.mesmaxlen,
                'picture': service.picture}

class Service(models.Model):
    ''' Абстрактный класс для всех сервисов '''
    active = models.BooleanField(verbose_name=_('Активность'), default=True)
    ouser = models.ForeignKey('ouser.OUser', verbose_name=_('Пользователь'))
    screen_name = models.CharField(verbose_name=_('Имя'), max_length=50, null=True, blank=True)
    
    objects = ServiceManager()
    
    class Meta:
        abstract = True
        app_label = 'ouser'

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.connection = self._get_connection()
        
    @property
    def user_name(self):
        return self.screen_name
    
    @property
    def ico(self):
        return 'img/services/%s.png' % self.slug
    
    @property
    def slug(self):
        return self.__class__.__name__.lower()
    
    @property
    def title(self):
        return self.__class__.__name__.title()
    
    @property
    def avatar_file(self):
        return os.path.join(settings.SERVICES_DIR, self.slug + '/avatars/' + hashlib.sha1(self.ouser.username).hexdigest() + '.png')
        
    @property
    def avatar_url(self):
        raise NotImplementedError("Your %s class has not defined a avatar_url() method, which is required." % self.__class__.__name__)  
    
    @property
    def picture(self):
        return '/media/services/%s/avatars/%s.png?%s' % (self.slug, hashlib.sha1(self.ouser.username).hexdigest(), datetime.datetime.now().isoformat()) 
    
    @property
    def mesmaxlen(self):
        raise NotImplementedError("Your %s class has not defined a mesmaxlen() method, which is required." % self.__class__.__name__)        

    def update_status(self, msg):
        """ Обновление статуса, максимальная длина сообщения 420 символов """
        if self.active:
            d = self.connection.UpdateStatus(msg.encode('utf-8'))
            if 'id' in d:
                return "Status updated"
            return "Can't update status"
        
    def _get_connection(self):
        raise NotImplementedError("Your %s class has not defined a _get_connection() method, which is required." % self.__class__.__name__)

    def save(self, *args, **kwargs):
        super(Service, self).save(*args, **kwargs)
        t = AvatarLoader(self.avatar_file, self.avatar_url)
        t.start()