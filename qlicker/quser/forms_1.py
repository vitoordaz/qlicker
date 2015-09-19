#-*- coding: utf-8 -*-
'''
Created on 10.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.conf import settings
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate

from models import RegistrationProfile, OUser

class SetPasswordForm(SetPasswordForm):
    '''
    Форма которая даёт пользователям возможность сменить пароль без .
    '''
    new_password1 = forms.CharField(label=_("Новый пароль:"), min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'text'}),
                                    error_messages={'required': _('Укажите пароль'),
                                                    'min_length': _('Длина пароля должна быть не менее 6 символов')})
    new_password2 = forms.CharField(label=_("Повтор пароля:"), min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'text'}),
                                    error_messages={'required': _('Укажите подтверждение пароля'),
                                                    'min_length': _('Длина пароля должна быть не менее 6 символов')})
    class Media:
        css = {'all': ('css/forms/set_password_form.css',)}
        js = ('js/forms/set_password_form.js',)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("Пароль и подтверждение не совпадают"))
        return password2

class PasswordResetForm(PasswordResetForm):
    '''
    Форма сброса пароля.
    '''
    email = forms.EmailField(label=_("Электронная почта:"),
                             widget=forms.TextInput(attrs={'class': 'text'}),
                             max_length=75,
                             error_messages={'required': _('Укажите адрес электронной почты')})

    class Media:
        css = {'all': ('css/forms/password_reset_form.css',)}
        js = ('js/forms/password_reset_form.js', )

    def clean_email(self):
        """
        Проверка что пользователь с таким email существует.
        """
        email = self.cleaned_data["email"]
        self.users_cache = OUser.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("Пользователь с таким адресом электронной почты не зарегистрирован"))
        return email

class ChagePasswordForm(forms.Form):
    '''
    Форма смены пароля.
    '''
    old_password = forms.CharField(label=_('Текущий пароль:'),
                                   widget=forms.PasswordInput(attrs={'class': 'text'}),
                                   min_length=6, max_length=128, required=True,
                                   error_messages={'required': _('Укажите текущий пароль'),
                                                   'min_length': _('Длина пароля должна быть не менее 6 символов')})
    new_password1 = forms.CharField(label=_('Новый пароль:'),
                                    widget=forms.PasswordInput(attrs={'class': 'text'}),
                                    min_length=6, max_length=128, required=True,
                                    error_messages={'required': _('Укажите новый пароль'),
                                                    'min_length': _('Длина пароля должна быть не менее 6 символов')})
    new_password2 = forms.CharField(label=_('Повтор пароля:'),
                                    widget=forms.PasswordInput(attrs={'class': 'text'}),
                                    min_length=6, max_length=128, required=True,
                                    error_messages={'required': _('Укажите подтверждение пароль'),
                                                    'min_length': _('Длина пароля должна быть не менее 6 символов')})

    class Media:
        css = {'all': ('css/forms/profile_password_change_form.css',)}
        js = ('js/forms/profile_password_change_form.js', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChagePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        '''
        Проверка предыдущего пароля.
        '''
        if not self.user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError(_('Текущий пароль не верен'))
        return self.cleaned_data['old_password']

    def clean_new_password2(self):
        '''
        Проверка паролей.
        '''
        if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
            raise forms.ValidationError(_('Введёные пароли не совпадают'))
        return self.cleaned_data['new_password2']

    def save(self):
        '''
        Изменение пароля.
        '''
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()

class LoadAvatarForm(forms.Form):
    '''
    Форма для загрузки аватара.
    '''
    avatar = forms.ImageField(label=_('Аватар'),
                              required=True,
                              error_messages={'required': _('Добавьте изображение'),
                                              'invalid_image': _('Файл который вы загрузили не является изображением')})
    class Media:
        css = {'all': ('css/forms/avatar_form.css',)}
        js = ('js/forms/avatar_form.js',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(LoadAvatarForm, self).__init__(*args, **kwargs)

    def save(self):
        self.user.avatar = self.cleaned_data['avatar']
        return self.user.save()

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
