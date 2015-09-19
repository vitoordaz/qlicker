import datetime
import hashlib
import random
import re

from django.conf import settings
from django.db import models
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from qlicker.quser.models import qlicker_user


SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationProfileManager(models.Manager):

    def activate_user(self, activation_key):
        """Activity user by activation key that sent to email."""
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if profile.is_activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = profile.ACTIVATED
                profile.save()
                return user
        return False

    @transaction.atomic
    def create_inactive_user(self, username, email, password, send_email=True):
        """Creates inactive user and sends activation email."""
        new_user = qlicker_user.QlickerUser.objects.create_user(username,
                                                                email,
                                                                password)
        new_user.is_active = False
        new_user.save()
        registration_profile = self.create_profile(new_user)
        if send_email:
            registration_profile.send_activation_email()
        return new_user

    def create_profile(self, user):
        salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha256(salt + user.username).hexdigest()
        return self.create(user=user, activation_key=activation_key)

    def abort_activation(self, activation_key):
        """Aborts registration activation email."""
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if (profile.activation_key != profile.ACTIVATED and
                  not profile.user.is_active):
                profile.user.delete()
                profile.delete()
                return True
        return False


class RegistrationProfile(models.Model):
    """Registration profile that keeps reference to user and activation key."""

    ACTIVATED = u'ACTIVATED'

    user = models.ForeignKey(qlicker_user.QlickerUser, verbose_name=_('User'),
                             unique=True)

    activation_key = models.CharField(_('Activation key'), max_length=40)

    objects = RegistrationProfileManager()

    class Meta:
        app_label = 'qlicker'
        db_table = 'registration_profile'
        verbose_name = 'Registration profile'
        verbose_name_plural = 'Registration profiles'

    def is_activation_key_expired(self):
        """This methods checks if activation key is expired."""
        expiration_days = datetime.timedelta(days=settings.ACTIVATION_DAYS)
        utcnow = datetime.datetime.utcnow()
        return not (self.activation_key == self.ACTIVATED or
                    self.user.date_joined + expiration_days <= utcnow)

    def send_activation_email(self):
        email_dict = {
            'activation_key': self.activation_key,
            'expiration_days': settings.ACTIVATION_DAYS
        }
        subject = render_to_string(
            'registration/activation_email_subject.html', email_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/activation_email.html',
                                   email_dict)
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
