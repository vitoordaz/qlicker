from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    code = models.CharField(_('Country code'), max_length=2)

    name = models.CharField(_('Name'), max_length=50)

    class Meta:
        app_label = 'qlicker'
        db_table = 'country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name', )

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)
