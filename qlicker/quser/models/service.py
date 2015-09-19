import datetime
import os
import hashlib
import json

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from qlicker import utils
from qlicker.quser.models import qlicker_user


class ServiceManager(models.Manager):

    def for_user(self, user):
        """Returns services that are associated with user."""
        try:
            return self.filter(active=True).get(ouser=user)
        except self.model.DoesNotExist:
            return None

    def active(self):
        """Returns all active services."""
        self.filter(active=True)


class ServiceJSONEncoder(json.JSONEncoder):
    """A custom JSON encoder for Service objects"""

    def default(self, service):
        if not isinstance (service, Service):
            raise ValueError('You cannot use the JSON custom '
                             'ServiceJSONEncoder for a non-Service object.')
        return {'user_name': service.user_name,
                'ico': service.ico,
                'slug': service.slug,
                'title': service.title,
                'mesmaxlen': service.mesmaxlen,
                'picture': service.picture}


class Service(models.Model):
    """Abstract class for all services."""

    active = models.BooleanField(verbose_name=_('Active'), default=True)

    user = models.ForeignKey(qlicker_user.QlickerUser, verbose_name=_('User'))

    screen_name = models.CharField(verbose_name=_('Name'), max_length=50,
                                   null=True, blank=True)

    objects = ServiceManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.connection = self._get_connection()

    @property
    def user_name(self):
        return self.screen_name

    @property
    def ico(self):
        return 'img/services/%s.png' % self.slug

    @property
    def slug(self):
        return self.__class__.__name__.lower()

    @property
    def title(self):
        return self.__class__.__name__.title()

    @property
    def avatar_file(self):
        filename = '%(slug)s/avatars/%(username)s.png' % {
            'slug': self.slug,
            'username': hashlib.sha1(self.ouser.username).hexdigest()
        }
        return os.path.join(settings.SERVICES_DIR, filename)

    @property
    def avatar_url(self):
        raise NotImplementedError(
            'Your %s class has not defined a avatar_url() method, which is '
            'required.' % self.__class__.__name__)

    @property
    def picture(self):
        return '/media/services/%(slug)s/avatars/%(username)s.png?%(date)s' % {
            'slug': self.slug,
            'username': hashlib.sha1(self.ouser.username).hexdigest(),
            'date': datetime.datetime.utcnow().isoformat()
        }

    @property
    def mesmaxlen(self):
        raise NotImplementedError(
            'Your %s class has not defined a mesmaxlen() method, which is '
            'required.' % self.__class__.__name__)

    def update_status(self, msg):
        """Updates status with a given message."""
        if self.active:
            d = self.connection.UpdateStatus(msg.encode('utf-8'))
            if 'id' in d:
                return 'Status updated'
            return 'Can\'t update status'

    def _get_connection(self):
        raise NotImplementedError(
            'Your %s class has not defined a _get_connection() method, which '
            'is required.' % self.__class__.__name__)

    def save(self, *args, **kwargs):
        super(Service, self).save(*args, **kwargs)
        utils.AvatarLoader(self.avatar_file, self.avatar_url).start()
