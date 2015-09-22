from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from qlicker.quser.models import qlicker_user


# class QlickerUserAdmin(UserAdmin):
#     fieldsets = ()
#
# admin.site.unregister(User)
# admin.site.register(qlicker_user.QlickerUser, QlickerUserAdmin)


# class FacebookAdmin(admin.ModelAdmin):
#     list_display = ('active', 'ouser', 'screen_name', 'user_id',)
#
#
# admin.site.register(Facebook, FacebookAdmin)
#
#
# class TwitterAdmin(admin.ModelAdmin):
#     list_display = ('active', 'ouser', 'screen_name',)
#
#
# admin.site.register(Twitter, TwitterAdmin)
