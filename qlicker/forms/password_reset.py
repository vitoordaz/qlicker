from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.utils.translation import gettext_lazy as _


class PasswordResetForm(BasePasswordResetForm):
    """Password reset form."""

    email = forms.EmailField(label=_('Email:'), max_length=75,
                             widget=forms.TextInput(attrs={'class': 'text'}),
                             error_messages={'required': _('Email required')})

    class Media:
        css = {'all': ('css/forms/password_reset_form.css',)}
        js = ('js/forms/password_reset_form.js', )

    def clean_email(self):
        """Checks if user with a given email already registered."""
        email = self.cleaned_data['email']
        self.users_cache = models.User.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_(
                'User with a given email is not registered'))
        return email
