from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from qlicker.quser.models import service
# from ouser import oauthfacebook


class Facebook(service.Service):

    access_token = models.CharField(verbose_name=_('Access token'),
                                    max_length=100)

    user_id = models.CharField(verbose_name=_('Facebook id'), max_length=20,
                               null=True, blank=True)

    class Meta:
        app_label = 'qlicker'
        db_table = 'facebook'
        verbose_name = 'Facebook access token'
        verbose_name_plural = 'Facebook access tokens'

    def __unicode__(self):
        return "%s %s %s" % (self.active, self.user_id, self.screen_name)

    def _get_connection(self):
        return oauthfacebook.OAuthApi(access_token=self.access_token)

    @property
    def avatar_url(self):
        return self.connection.getPicture(settings.FB_PICTURE_TYPE)

    @property
    def mesmaxlen(self):
        return 420

    def update_status(self, msg):
        return super(Facebook, self).update_status(msg)
