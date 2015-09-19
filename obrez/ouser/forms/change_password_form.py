#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from django import forms
from django.utils.translation import gettext_lazy as _

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