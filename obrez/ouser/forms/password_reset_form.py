#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext_lazy as _

from ouser.models import OUser

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