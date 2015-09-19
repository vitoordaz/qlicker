#-*- coding: utf-8 -*-
'''
Created on 10.02.2010

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import OUser, Facebook, Twitter

class OUserAdmin(UserAdmin):
    fieldsets = ()

class FacebookAdmin(admin.ModelAdmin):
    list_display = ('active', 'ouser', 'screen_name', 'user_id',)

class TwitterAdmin(admin.ModelAdmin):
    list_display = ('active', 'ouser', 'screen_name',)

admin.site.unregister(User)
admin.site.register(OUser, OUserAdmin)
admin.site.register(Facebook, FacebookAdmin)
admin.site.register(Twitter, TwitterAdmin)