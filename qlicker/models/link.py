import re
import urllib
import datetime

from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.safestring import mark_for_escaping
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from qlicker import utils


HOST = re.compile(
    r'^(https?://)?' # http:// or https://
    r'(www\.)?'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?', re.IGNORECASE) # optional port


class LinksManager(models.Manager):

    def archived(self, user):
        q = self.filter(archived=True).order_by('-updated_at')
        return q.filter(owner=user)

    def for_user(self, user):
        q = self.filter(archived=False).order_by('-updated_at')
        return q.filter(owner=user)


class Link(models.Model):
    archived = models.BooleanField(verbose_name=_('Archived'), default=False)

    url = models.URLField(verbose_name=_('URL'))

    code = models.CharField(verbose_name=_('Code'), max_length=10,
                            null=True, blank=True, editable=False)

    redirects = models.IntegerField(verbose_name=_('Redirects'), default=0,
                                    help_text=_('Number of redirects'),
                                    null=True)

    owner = models.ForeignKey(auth_models.User, verbose_name=_('Owner'),
                              null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    title = models.CharField(verbose_name=_('URL title'), max_length=150,
                             blank=True, null=True)

    objects = LinksManager()

    class Meta:
        app_label = 'qlicker'
        db_table = 'link'
        verbose_name = u'Link'
        verbose_name_plural = u'Links'
        ordering = ('-updated_at', '-id')

    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            kwargs['url'] = utils.normalize_url(kwargs['url'])
        super(Link, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return str(self.url)

    @property
    def favicon(self):
        return '%sfavicon/%s.png' % (settings.MEDIA_URL, self.code)

    @property
    def qlink(self):
        return '%s/%s' % (settings.SITE_URL, self.code)

    @property
    def long(self):
        return urllib.unquote(self.url.encode('utf-8'))

    def set_title(self, title):
        self.title = mark_for_escaping(title)

    def recover(self):
        self.archived = False

    def updated_now(self):
        self.updated_at = datetime.datetime.utcnow()

    def increment_redirects(self):
        self.redirects += 1

    def save(self, **kwargs):
        super(Link, self).save(**kwargs)
        if not self.code:
            self.code = utils.encode(self.id)
            # qr = QRCodeGen(self.code)  # generate qr code
            # qr.start()
            # if self.user:
            #     get_link_meta(self)
            # else:
            #     m = threading.Thread(target=get_link_meta, name='t1',
            #                          args=[self])
            #     m.start()
            super(Link, self).save()

    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'qlink': self.qlink,
            'favicon': self.favicon,
            'title': self.title,
            'created_at': utils.datetime2timestamp(self.created_at),
            'redirects': self.redirects
        }
