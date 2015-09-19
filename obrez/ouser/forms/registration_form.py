#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django import forms
from django.utils.translation import gettext_lazy as _

from ouser.models import OUser, RegistrationProfile

class RegistrationForm(forms.Form):
    '''
    Форма регистрации пользователя.
    '''
    username = forms.SlugField(label=_('Логин:'),
                               widget=forms.TextInput(attrs={'class': 'text'}),
                               min_length=4,
                               max_length=30,
                               required=True,
                               error_messages={'required': _('Укажите логин'),
                                               'min_length': _('Длина логина должна быть не менее 4 символов'),
                                               'invalid': _('Логин должен состоять только из букв, цифр, знаков подчеркивания или дефиса.')})
    email = forms.EmailField(label=_('Электронная почта:'),
                             widget=forms.TextInput(attrs={'class': 'text'}),
                             required=True,
                             error_messages={'required': _('Укажите адрес электронной почты'),
                                             'invalid': _('Укажите правильный адрес электронной почты')})

    password1 = forms.CharField(label=_('Пароль:'),
                                widget=forms.PasswordInput(attrs={'class': 'text'}),
                                min_length=6,
                                max_length=128,
                                required=True,
                                error_messages={'required': _('Укажите пароль'),
                                                'min_length': _('Длина пароля должна быть не менее 6 символов')})
    password2 = forms.CharField(label=_('Повтор пароля:'),
                                widget=forms.PasswordInput(attrs={'class': 'text'}),
                                min_length=6,
                                max_length=128,
                                required=True,
                                error_messages={'required': _('Укажите подтверждение пароля'),
                                                'min_length': _('Длина пароля должна быть не менее 6 символов')})
    news = forms.BooleanField(label=_('Получать новости проекта?'),
                              required=False,
                              widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))

    class Media:
        css = {'all': ('css/forms/registration_form.css',)}
        js = ('js/forms/registration_form.js',)

    def clean_username(self):
        '''
        Проверка имени пользователя. Имя пользователя должно быть уникальным.
        '''
        try:
            user = OUser.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError(_('Пользователь с таким логином уже существует'))
        except OUser.DoesNotExist:
            return self.cleaned_data['username']

    def clean_email(self):
        '''
        Проверка email. Email должен быть уникальным.
        '''
        try:
            user = OUser.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError(_('Такой адрес электронной почты используется'))
        except OUser.DoesNotExist:
            return self.cleaned_data['email']

    def clean_password2(self):
        '''
        Проверка паролей.
        '''
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_('Введёные пароли не совпадают'))
        return self.cleaned_data['password2']

    def save(self, commit=True):
        RegistrationProfile.objects.create_inactive_user(self.cleaned_data['username'],
                                                         self.cleaned_data['email'],
                                                         self.cleaned_data['password1'])
        return True
