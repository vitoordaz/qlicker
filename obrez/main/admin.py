#-*- coding: utf-8 -*-
'''
Created on 05.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.contrib import admin
from models import Links, Country, GeoIPdb, Redirects

class LinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'inarchive', 'created_at', 'user', 'url', 'counter', )

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class GeoIPdbAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'country')

class RedirectsAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'created_at', 'link', 'country', 'referrer', 'domain', 'path')

admin.site.register(Links, LinksAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(GeoIPdb, GeoIPdbAdmin)
admin.site.register(Redirects, RedirectsAdmin)