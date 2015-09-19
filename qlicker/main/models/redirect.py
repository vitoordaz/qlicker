import time
import json
import urlparse
import datetime

from django.db.models import Count
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from qlicker import utils
from qlicker.main.models import country
from qlicker.main.models import link
from qlicker.main.models import geoipdb


class RedirectsManager(models.Manager):

    def for_link(self, link):
        return self.filter(link=link)

    def stat(self, typ, link, timestamp=None, hourly=False):
        if typ == 'clicks':
            values = ('date', ) if not hourly else ('created_at', )
            count = 'date'
            order = 'date'
        elif typ == 'domains':
            values = ('domain', )
            count = 'referrer'
            order = '-clicks'
        elif typ == 'countries':
            values = ('country__code', )
            count = 'country'
            order = '-clicks'
        elif typ == 'referrer':
            values = ('domain', 'referrer', )
            count = 'referrer'
            order = '-clicks'
        else:
          raise ValueError('Invalid type: %s' % typ)

        if not timestamp:
            q = self.for_link(link).values(*values)
            q = q.annotate(clicks=Count(count)).order_by(order)
            return q

        q = self.for_link(link).exclude(created_at__lt=timestamp)
        q = q.values(*values).annotate(clicks=Count(count)).order_by(order)
        return q

    def make_referer(self, referer):
        try:
            vurl = URLValidator(False)
            vurl(referer)
            referer = utils.normalize_url(referer)
            pr = urlparse.urlsplit(referer)
            domain = pr.netloc[:60]
            pr = list(pr)
            pr[0] = pr[1] = ''
            path = urlparse.urlunsplit(pr)[:255]
        except ValidationError:
            domain = path = ''
        return referer, domain, path

    def create_redirect(self, link, request):
        link.inc_counter()
        link.save()

        referer = request.META.get('HTTP_REFERER', '')
        referrer, domain, path = self.make_referer(referer)

        ip = request.META.get('REMOTE_ADDR', None)
        country = geoipdb.GeoIPdb.objects.get_country(ip)

        return self.create(link=link, country=country, referrer=referrer,
                           domain=domain, path=path)


class Redirect(models.Model):
    link = models.ForeignKey(link.Link, verbose_name=_('Link'))

    date = models.DateField(_('Redirect date'), auto_now=True,
                            default=datetime.datetime.utcnow())

    time = models.TimeField(_('Redirect time'), auto_now=True,
                            default=datetime.datetime.utcnow())

    created_at = models.DateTimeField(_('Created at'), auto_now=True,
                                      default=datetime.datetime.utcnow())

    country = models.ForeignKey(country.Country, verbose_name=_('Country'),
                                null=True)

    domain = models.CharField(_('Domen'), max_length=60, blank=True)

    path = models.CharField(_('Path'), max_length=255, blank=True)

    referrer = models.URLField(_('Referrer'), verify_exists=False, blank=True)

    ip = models.IPAddressField(_('IP'), blank=True, null=True)

    browser = models.CharField(_('Browser'), max_length=255, null=True)

    objects = RedirectsManager()

    class Meta:
        app_label = 'qlicker'
        db_table = 'redirect'
        verbose_name = 'Redirect'
        verbose_name_plural = 'Redirects'

    def __unicode__(self):
        return u"%s" % self.country

    def get_absolute_url(self):
        return reverse('redirect', self.link.code)

    @property
    def timestamp(self):
        return time.mktime(self.date.timetuple())


class RedirectsClicksJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj


class RedirectsCountriesJSONEncoder(json.JSONEncoder):
    def default(self, redirects):
        return [{'code': redirect['country__code'],
                 'clicks': redirect['clicks']} for redirect in redirects ]


class RedirectsDomainsJSONEncoder(json.JSONEncoder):
    """A custom JSON encoder for Redirects domains objects."""
    def default(self, redirects):
        return [{'domain': redirect['domain'],
                 'clicks': redirect['clicks']} for redirect in redirects]


class RedirectsReferrerJSONEncoder(json.JSONEncoder):
    """A custom JSON encoder for Redirects referrer objects."""

    def default(self, redirects):
        p = {}
        for redirect in redirects:
            if redirect['domain'] not in p:
                p[redirect['domain']] = []
            p[redirect['domain']].append({'referrer': redirect['referrer'],
                                          'clicks': redirect['clicks']})
        return p


def create_redirect(link, request):
    Redirect.objects.create_redirect(link, request)
