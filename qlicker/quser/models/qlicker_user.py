import hashlib
import urllib

from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.utils.translation import gettext_lazy as _

from qlicker.quser.forms.fields import resize_image
from twitter import Twitter
from facebook import Facebook


class QlickerUser(User):
    avatar = resize_image.ResizeImageField(
        verbose_name=_('Avator'), new_width=settings.DEFAULT_AVATAR_WIDTH,
        new_height=settings.DEFAULT_AVATAR_HEIGHT, upload_to='avatars',
        blank=True)

    objects = UserManager()

    class Meta:
        app_label = 'qlicker'
        db_table = 'qlicker_user'
        verbose_name = u'User'
        verbose_name_plural = u'Users'

    def get_avatar(self):
        """This method returns user's avatar."""
        if self.avatar:
            return '/media/avatars/%s' % self.avatar.name
        return 'http://www.gravatar.com/avatar/%(id)s?%(params)s' % {
            'id': hashlib.md5(self.email.lower().strip()).hexdigest(),
            'params': urllib.urlencode({
                'd': settings.DEFAULT_AVATAR,
                's': str(settings.DEFAULT_AVATAR_SIZE)
            })
        }

    @property
    def services(self):
        """Returns a list of user services."""
        if 'service_list' not in self.__dict__:
            self.service_list = []
            try:
                self.service_list.append(Twitter.objects.get(ouser=self))
            except Twitter.DoesNotExist:
                pass
            try:
                self.service_list.append(Facebook.objects.get(ouser=self))
            except Facebook.DoesNotExist:
                pass
        return self.service_list

    @property
    def active_services(self):
        """Returns a list of active user services."""
        return [service for service in self.services if service.active]

    def update_status(self, msg):
        """This method updates user status on connected services."""
        status = {}
        fb = Facebook.objects.for_user(self)
        if fb:
            status['facebook'] = fb.update_status(msg)
        tw = Twitter.objects.for_user(self)
        if tw:
            status['twitter'] = tw.update_status(msg)
        return status
