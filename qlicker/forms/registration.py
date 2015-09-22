from django import forms
from django.contrib.auth import models
from django.utils.translation import gettext_lazy as _

from qlicker.models import registration_profile


class RegistrationForm(forms.Form):
    """User registration form."""

    username = forms.SlugField(
        label=_('Username:'), widget=forms.TextInput(attrs={'class': 'text'}),
        min_length=4, max_length=30, required=True,
        error_messages={
            'required': _('Username required'),
            'min_length': _('Username should be at least 4 symbols'),
            'invalid': _('Invalid username')
        })

    email = forms.EmailField(
        label=_('Email:'), widget=forms.TextInput(attrs={'class': 'text'}),
        required=True,
        error_messages={'required': _('Email required'),
                        'invalid': _('Invalid email address')})

    password1 = forms.CharField(
        label=_('Password:'),
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        min_length=6, max_length=128, required=True,
        error_messages={'required': _('Password required'),
                        'min_length': _('Password length should be at lease 6 '
                                        'symbols')})

    password2 = forms.CharField(
        label=_('Password repeat:'),
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        min_length=6, max_length=128, required=True,
        error_messages={'required': _('Password repeat required'),
                        'min_length': _('Password length should be at lease 6 '
                                        'symbols')})

    class Media:
        css = {'all': ('css/forms/registration_form.css',)}
        js = ('js/forms/registration_form.js',)

    def clean_username(self):
        """Validates username, it should unique."""
        try:
            username = self.cleaned_data['username']
            models.User.objects.get(username=username)
            raise forms.ValidationError(_(
                'User with this username already exist'))
        except models.User.DoesNotExist:
            return self.cleaned_data['username']

    def clean_email(self):
        """Validates email, it should unique."""
        try:
            models.User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError(_(
                'User with a given email already registered'))
        except models.User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_password2(self):
        """Validates given passwords."""
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_('Given passwords are not equal'))
        return self.cleaned_data['password2']

    def save(self, commit=True):
        registration_profile.RegistrationProfile.objects.create_inactive_user(
            self.cleaned_data['username'], self.cleaned_data['email'],
            self.cleaned_data['password1'])
        return True
