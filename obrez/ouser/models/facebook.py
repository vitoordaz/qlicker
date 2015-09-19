#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.orddaz@gmail.com>
'''
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from service import Service
from ouser import oauthfacebook

class Facebook(Service):
    '''
    Facebook --- класс модели для хранения ключей аккаунтов facebook.
    '''
    access_token = models.CharField(verbose_name=_('Access token'), max_length=100)
    user_id = models.CharField(verbose_name=_('Facebook id'), max_length=20, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Доступ к аккаунтам facebook'
        verbose_name_plural = 'Доступы к аккаунтам facebook'
        app_label = 'ouser'
        
    def __unicode__(self):
        return "%s %s %s" % (self.active, self.user_id, self.screen_name)
    
    def _get_connection(self):
        return oauthfacebook.OAuthApi(access_token=self.access_token)
    
    @property
    def avatar_url(self):
        return self.connection.getPicture(settings.FB_PICTURE_TYPE)
    
    @property
    def mesmaxlen(self):
        return 420
       
    def update_status(self, msg):
        """ Обновление статуса, максимальная длина сообщения 420 символов """
        return super(Facebook, self).update_status(msg)