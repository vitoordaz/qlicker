#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from service import Service

from ouser import oauthtwitter

class Twitter(Service):
    '''
    Twitter --- класс модели для хранения ключей аккаунтов twitter.
    '''
    oauth_token = models.CharField(verbose_name=_('Oauth token'), max_length=60)
    oauth_token_secret = models.CharField(verbose_name=_('Oauth token secret'), max_length=60)

    class Meta:
        verbose_name = 'Доступ к аккаунтам twitter'
        verbose_name_plural = 'Доступы к аккаунтам twitter'
        app_label = 'ouser'

    def __unicode__(self):
        return "%s %s" % (self.active, self.screen_name)
    
    def _get_connection(self):
        return oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY, 
                                     settings.TWITTER_CONSUMER_SECRET,
                                     self.oauth_token, 
                                     self.oauth_token_secret)
    
    @property
    def avatar_url(self):
        return "http://api.twitter.com/1/users/profile_image/%s.json?size=%s" % (self.screen_name, settings.TWITTER_PICTURE_SIZE) 
    
    @property
    def mesmaxlen(self):
        return 140
    
    def update_status(self, msg):
        """ Обновление статуса, максимальная длина сообщения 140 символов """
        return super(Twitter, self).update_status(msg)  
