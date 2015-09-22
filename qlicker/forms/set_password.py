from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _


class SetPasswordForm(auth_forms.SetPasswordForm):
    """User set password form."""

    new_password1 = forms.CharField(
        label=_('New password'), min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        error_messages={'required': _('Password required'),
                        'min_length': _('Password length should be at lease 6 '
                                        'symbols')})

    new_password2 = forms.CharField(
        label=_('Password repeat:'), min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        error_messages={'required': _('Password repeat required'),
                        'min_length': _('Password length should be at lease 6 '
                                        'symbols')})

    class Media:
        css = {'all': ('css/forms/set_password_form.css',)}
        js = ('js/forms/set_password_form.js',)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_('Passwords are not equal'))
        return password2
