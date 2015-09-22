from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from qlicker.models import service


class Twitter(service.Service):
    """This service stores information about twitter oAuth token."""

    oauth_token = models.CharField(verbose_name=_('Oauth token'),
                                   max_length=60)

    oauth_token_secret = models.CharField(verbose_name=_('Oauth token secret'),
                                          max_length=60)

    class Meta:
        app_label = 'qlicker'
        verbose_name = 'Auth token for Twitter'
        verbose_name_plural = 'Auth tokens for Twitter'

    def __unicode__(self):
        return "%s %s" % (self.active, self.screen_name)

    def _get_connection(self):
        return oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY,
                                     settings.TWITTER_CONSUMER_SECRET,
                                     self.oauth_token,
                                     self.oauth_token_secret)

    @property
    def avatar_url(self):
        return (
            'http://api.twitter.com/1/users/profile_image/%(username)s.json?'
            'size=%(size)s' % {
                'username': self.screen_name,
                'size': settings.TWITTER_PICTURE_SIZE
            }
        )

    @property
    def mesmaxlen(self):
        return 140

    def update_status(self, msg):
        """Updates user's status, message max length is 140."""
        return super(Twitter, self).update_status(msg)
