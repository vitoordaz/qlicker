#-*- coding: utf-8 -*-
'''
Created on 16.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models.country import Country

class GeoIPdbManager(models.Manager):
    def get_country(self, ip):
        '''
        Определение страны по ip
        '''
        try:
            return self.extra(tables = ['main_geoipdb'],
                              where=["%s between main_geoipdb.start and main_geoipdb.end"],
                              params=[ip])[0].country
        except IndexError:
            return Country.objects.get(code='??')# undefined country

class GeoIPdb(models.Model):
    '''
    GeoIPdb --- класс модели для хранения базы данных интервалов ip адрессов.
    '''
    start = models.IPAddressField(_('Начало диапазона'))
    end = models.IPAddressField(_('Конец диапазона'))
    country = models.ForeignKey(Country)

    objects = GeoIPdbManager()

    class Meta:
        db_table = 'main_geoipdb'
        verbose_name = _('Geo IP db')
        verbose_name_plural = _('Geo IP db')
        app_label = 'main'

    def __unicode__(self):
        return "%s-%s" % (self.start, self.end)