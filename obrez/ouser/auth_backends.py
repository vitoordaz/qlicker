#-*- coding: utf-8 -*-
'''
Created on 10.02.2010

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from models import OUser
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured

class OUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None 
    
    @property 
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = OUser
            if not self._user_class:
                raise ImproperlyConfigured(_('Could not get custom user model'))
        return self._user_class