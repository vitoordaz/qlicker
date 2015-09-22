# import hashlib
# import urllib
#
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.utils.translation import gettext_lazy as _
#
# from qlicker.quser.forms.fields import resize_image
# from qlicker.models import facebook
# from qlicker.models import twitter
#
#
# class QlickerUser(AbstractUser):
#
#     avatar = resize_image.ResizeImageField(
#         verbose_name=_('Avatar'), new_width=settings.DEFAULT_AVATAR_WIDTH,
#         new_height=settings.DEFAULT_AVATAR_HEIGHT, upload_to='avatars',
#         blank=True)
#
#     class Meta:
#         app_label = 'qlicker'
#         db_table = 'qlicker_user'
#         verbose_name = u'User'
#         verbose_name_plural = u'Users'
#
#     def get_avatar(self):
#         """This method returns user's avatar."""
#         if self.avatar:
#             return '/media/avatars/%s' % self.avatar.name
#         return 'http://www.gravatar.com/avatar/%(id)s?%(params)s' % {
#             'id': hashlib.md5(self.email.lower().strip()).hexdigest(),
#             'params': urllib.urlencode({
#                 'd': settings.DEFAULT_AVATAR,
#                 's': str(settings.DEFAULT_AVATAR_SIZE)
#             })
#         }
#
#     @property
#     def services(self):
#         """Returns a list of user services."""
#         if 'service_list' not in self.__dict__:
#             self.service_list = []
#             try:
#                 self.service_list.append(
#                     twitter.Twitter.objects.get(ouser=self))
#             except twitter.Twitter.DoesNotExist:
#                 pass
#             try:
#                 self.service_list.append(
#                     facebook.Facebook.objects.get(ouser=self))
#             except facebook.Facebook.DoesNotExist:
#                 pass
#         return self.service_list
#
#     @property
#     def active_services(self):
#         """Returns a list of active user services."""
#         return [service for service in self.services if service.active]
#
#     def update_status(self, msg):
#         """This method updates user status on connected services."""
#         status = {}
#         fb = facebook.Facebook.objects.for_user(self)
#         if fb:
#             status['facebook'] = fb.update_status(msg)
#         tw = twitter.Twitter.objects.for_user(self)
#         if tw:
#             status['twitter'] = tw.update_status(msg)
#         return status
