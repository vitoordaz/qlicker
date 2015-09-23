from django.db import models
from django.utils.translation import gettext_lazy as _

from qlicker.models import country


class GeoIPdbManager(models.Manager):

    def get_country(self, ip):
        """Returns country by ip address."""
        try:
            return self.extra(
                tables=['geoipdb'],
                where=['%s between geoipdb.start and geoipdb.end'],
                params=[ip])[0].country
        except IndexError:
            return country.Country.objects.get(code='??')  # undefined country


class GeoIPdb(models.Model):
    """This models keeps IP address intervals for a countries."""

    start = models.GenericIPAddressField(_('Beginning of IP address interval'))

    end = models.GenericIPAddressField(_('End of IP address interval'))

    country = models.ForeignKey(country.Country)

    objects = GeoIPdbManager()

    class Meta:
        app_label = 'qlicker'
        db_table = 'geoipdb'
        verbose_name = _('Geo IP db')
        verbose_name_plural = _('Geo IP db')

    def __unicode__(self):
        return "%s-%s" % (self.start, self.end)
