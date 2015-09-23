from django.contrib import admin

from qlicker.models import facebook
from qlicker.models import link
from qlicker.models import registration_profile
from qlicker.models import twitter


admin.site.register(registration_profile.RegistrationProfile)


class FacebookAdmin(admin.ModelAdmin):
    list_display = ('active', 'user', 'screen_name', 'user_id',)


admin.site.register(facebook.Facebook, FacebookAdmin)


class TwitterAdmin(admin.ModelAdmin):
    list_display = ('active', 'user', 'screen_name',)


admin.site.register(twitter.Twitter, TwitterAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'owner', 'created_at')


admin.site.register(link.Link, LinkAdmin)
