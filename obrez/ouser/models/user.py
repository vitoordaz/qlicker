#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import hashlib, urllib

from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.utils.translation import gettext_lazy as _

from main.fields import ResizeImageField
from twitter import Twitter
from facebook import Facebook

class OUser(User):
    '''
    OUser: класс пользователя
    @ivar avatar: аватар пользователя, уменьшается сам
    '''
    avatar = ResizeImageField(verbose_name=_('Аватар'), new_width=settings.DEFAULT_AVATAR_WIDTH,
                              new_height=settings.DEFAULT_AVATAR_HEIGHT, upload_to='avatars', blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
        app_label = 'ouser'

    def get_avatar(self):
        '''
        Метод возвращает url аватара на сервере или ссылку на Gravatar.
        '''
        if self.avatar:
            return "/media/avatars/%s" % (self.avatar.name) #TODO: change it!
        else:
            return "http://www.gravatar.com/avatar/%s?%s" % \
                (hashlib.md5(self.email.lower().strip()).hexdigest(),
                 urllib.urlencode({'d': settings.DEFAULT_AVATAR, 's': str(settings.DEFAULT_AVATAR_SIZE)}))
                
    @property
    def services(self):
        """ Возвращает сервисы привязанные к пользователю """
        if 'service_list' not in self.__dict__:
            self.service_list = []
            try:
                self.service_list.append(Twitter.objects.get(ouser=self))
            except Twitter.DoesNotExist:
                pass
            try:
                self.service_list.append(Facebook.objects.get(ouser=self))
            except Facebook.DoesNotExist:
                pass
        return self.service_list

    @property
    def active_services(self):
        """ Возвращает толко активные сервисы привязанные к пользователю """
        return [service for service in self.services if service.active]
    
    def update_status(self, msg):
        """ Обновляет статус пользователя в сервисах """
        status = {}
        fb = Facebook.objects.for_user(self)
        if fb:
            status['facebook'] = fb.update_status(msg)
        tw = Twitter.objects.for_user(self)
        if tw:
            status['twitter'] = tw.update_status(msg)
        return status