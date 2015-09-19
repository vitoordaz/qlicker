#-*- coding: utf-8 -*-
'''
Created on 23.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django import forms
from django.utils.translation import gettext_lazy as _

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