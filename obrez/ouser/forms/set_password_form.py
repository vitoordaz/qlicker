#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

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