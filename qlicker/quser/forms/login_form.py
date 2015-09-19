#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    '''
    Изменяем имя поля.
    '''
    username = forms.SlugField(label=_('Логин:'),
                               widget=forms.TextInput(attrs={'class': 'text'}),
                               max_length=30,
                               error_messages={'required': _('Укажите логин')})
    password = forms.CharField(label=_('Пароль:'),
                               widget=forms.PasswordInput(attrs={'class': 'text'}),
                               error_messages={'required': _('Укажите пароль')})

    class Media:
        css =  {'all': ('css/forms/login_form.css',)}
        js = ('js/forms/login_form.js', )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username and not password:
            raise forms.ValidationError(_('Укажите логин и пароль'))

        self.user_cache = authenticate(username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError(_('Укажите правильный логин и пароль'))
        elif not self.user_cache.is_active:
            raise forms.ValidationError(_('Учётная запись пользователя не активирована'))
        super(LoginForm, self).clean()
