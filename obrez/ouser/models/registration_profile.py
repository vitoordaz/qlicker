#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import re, random, datetime

from django.conf import settings
from django.db import models, transaction
from django.utils.hashcompat import sha_constructor
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from user import OUser

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class RegistrationProfileManager(models.Manager):
    '''
    Менеджер для работы с профайлами регистрации.
    '''
    def activate_user(self, activation_key):
        '''
        Активация пользователя по ключу активации отправленного по email.
        '''
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if profile.is_activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = profile.ACTIVATED
                profile.save()
                return user
        return False

    def create_inactive_user(self, username, email, password, send_email=True):
        '''
        Создает неактивного пользователя и профайл регистрации для него.
        Поумолчанию отправляется письмо с ключом активации.
        '''
        new_user = OUser.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()
        registration_profile = self.create_profile(new_user)
        if send_email:
            registration_profile.send_activation_email()
        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user):
        '''
        Создание RegistrationProfile для пользователя (user).
        '''
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(salt + user.username).hexdigest()
        return self.create(user=user, activation_key=activation_key)

    def abort_activation(self, activation_key):
        '''
        Отмена регистрации пользователя Активация пользователя по ключу активации отправленного по email.
        '''
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if profile.activation_key != profile.ACTIVATED and not profile.user.is_active:
                profile.user.delete()
                profile.delete()
                return True
        return False

class RegistrationProfile(models.Model):
    '''
    RegistrationProfile: класс профиля регистрации хранит пользователя и ключ активации.
    user: польщователь
    activation_key: ключ активации пользователя
    '''
    ACTIVATED = u'ACTIVATED'

    user = models.ForeignKey(OUser, unique=True, verbose_name=_('Пользователь'))
    activation_key = models.CharField(_('Ключ активации'), max_length=40)

    objects = RegistrationProfileManager()

    class Meta:
        verbose_name = 'Профайл регистрации'
        verbose_name_plural = 'Профайлы регистрации'
        app_label = 'ouser'

    def is_activation_key_expired(self):
        '''
        Метод для определения является ли ключ активации действительным.
        '''
        expiration_days = datetime.timedelta(days=settings.ACTIVATION_DAYS)
        return not (self.activation_key == self.ACTIVATED or self.user.date_joined + expiration_days <= datetime.datetime.now())

    def send_activation_email(self):
        email_dict = {
                      'activation_key': self.activation_key,
                      'expiration_days': settings.ACTIVATION_DAYS}
        subject = render_to_string('registration/activation_email_subject.html', email_dict)
        #Email не должно содержать переносов
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/activation_email.html', email_dict)
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)