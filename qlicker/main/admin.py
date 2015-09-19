from django.contrib import admin

from qlicker.main.models import country
from qlicker.main.models import geoipdb
from qlicker.main.models import link
from qlicker.main.models import redirect


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'archived', 'created_at', 'user', 'url',
                    'redirects', )


admin.site.register(link.Link, LinkAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(country.Country, CountryAdmin)


class GeoIPdbAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'country')


admin.site.register(geoipdb.GeoIPdb, GeoIPdbAdmin)


class RedirectAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'created_at', 'link', 'country',
                    'referrer', 'domain', 'path')


admin.site.register(redirect.Redirect, RedirectAdmin)
