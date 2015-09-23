import time
import json
import urlparse

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from qlicker import utils
from qlicker.models import country
from qlicker.models import link
from qlicker.models import geoipdb


class RedirectsManager(models.Manager):

    def for_link(self, l):
        """Returns a redirects query for a given link."""
        return self.filter(link=l)

    def stat(self, l):
        # if typ == 'clicks':
        #     values = ('date', ) if not hourly else ('created_at', )
        #     count = 'date'
        #     order = 'date'
        # elif typ == 'domains':
        #     values = ('domain', )
        #     count = 'referrer'
        #     order = '-clicks'
        # elif typ == 'countries':
        #     values = ('country__code', )
        #     count = 'country'
        #     order = '-clicks'
        # elif typ == 'referrer':
        #     values = ('domain', 'referrer', )
        #     count = 'referrer'
        #     order = '-clicks'
        # else:
        #     raise ValueError('Invalid type: %s' % typ)

        # if not timestamp:
        #     q = self.for_link(l).values(*values)
        #     q = q.annotate(clicks=models.Count(count)).order_by(order)
        #     return q
        #
        # q = self.for_link(link).exclude(created_at__lt=timestamp)
        # q = q.values(*values).annotate(clicks=models.Count(count))
        # return q.order_by(order)

        return {
            'redirects': [{
                'date': utils.datetime2timestamp(i['date']),
                'redirects': i['redirects']
            } for i in self.for_link(l).values('date')
                .annotate(redirects=models.Count('date'))
                .order_by('date')
            ],
            'countries': [{
                'country': i['country__code'],
                'redirects': i['redirects']
            } for i in self.for_link(l).values('country__code')
                .annotate(redirects=models.Count('country'))
                .order_by('-redirects')
            ],
            'domains': [{
                'domain': i['domain'],
                'redirects': i['redirects']
            } for i in self.for_link(l).values('domain')
                .annotate(redirects=models.Count('referrer'))
                .order_by('-redirects')
            ],
            'referrer': [{
                'referrer': i['referrer'],
                'redirects': i['redirects']
            } for i in self.for_link(l).values('domain', 'referrer')
                .annotate(redirects=models.Count('referrer'))
                .order_by('-redirects')
            ]
        }

    def make_referer(self, referer):
        try:
            vurl = URLValidator()
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

    def create_redirect(self, l, request):
        """Creates redirect object for a given link and HTTP request."""
        l.increment_redirects()
        l.save()
        d = {'link': l}

        referer = request.META.get('HTTP_REFERER', '')
        d['referrer'], d['domain'], d['path'] = self.make_referer(referer)

        ip = request.META.get('REMOTE_ADDR', None)
        d['country'] = geoipdb.GeoIPdb.objects.get_country(ip)

        return self.create(**d)


class Redirect(models.Model):
    link = models.ForeignKey(link.Link, verbose_name=_('Link'))

    date = models.DateField(_('Redirect date'), auto_now=True)

    time = models.TimeField(_('Redirect time'), auto_now=True)

    created_at = models.DateTimeField(_('Created at'), auto_now=True)

    country = models.ForeignKey(country.Country, verbose_name=_('Country'),
                                null=True)

    domain = models.CharField(_('Domen'), max_length=60, blank=True)

    path = models.CharField(_('Path'), max_length=255, blank=True)

    referrer = models.URLField(_('Referrer'), blank=True)

    ip = models.GenericIPAddressField(_('IP'), blank=True, null=True)

    browser = models.CharField(_('Browser'), max_length=255, null=True)

    objects = RedirectsManager()

    class Meta:
        app_label = 'qlicker'
        db_table = 'redirect'
        verbose_name = 'Redirect'
        verbose_name_plural = 'Redirects'

    def __unicode__(self):
        return '%s' % self.country

    def get_absolute_url(self):
        return reverse('redirect', self.link.code)

    @property
    def timestamp(self):
        return time.mktime(self.date.timetuple())


def create_redirect(l, request):
    Redirect.objects.create_redirect(l, request)
