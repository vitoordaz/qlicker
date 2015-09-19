#-*- coding: utf-8 -*-
'''
Created on 16.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    '''
    Country --- класс модели для хранения стран.
    '''
    code = models.CharField(_('Код страны'), max_length=2)
    name = models.CharField(_('Название'), max_length=50)
    #name_ru = models.CharField(_('Название рус'), max_length=70)

    class Meta:
        db_table = 'main_country'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        app_label = 'main'
        ordering = ('name', )

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.code)