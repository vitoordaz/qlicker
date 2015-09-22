from django import forms
from django.utils.translation import gettext_lazy as _


class PasswordChangeForm(forms.Form):
    """Password change form."""

    old_password = forms.CharField(
        label=_('Current password:'),
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        min_length=6, max_length=128, required=True,
        error_messages={'required': _('Current password required'),
                        'min_length': _('Password length should be at least 6 '
                                        'symbols')})

    new_password1 = forms.CharField(
        label=_('New password:'),
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        min_length=6, max_length=128, required=True,
        error_messages={'required': _('New password required'),
                        'min_length': _('Password length should be at least 6 '
                                        'symbols')})

    new_password2 = forms.CharField(
        label=_('Password repeat:'),
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        min_length=6, max_length=128, required=True,
        error_messages={'required': _('Password repeat required'),
                        'min_length': _('Password length should be at least 6 '
                                        'symbols')})

    class Media:
        css = {'all': ('css/forms/profile_password_change_form.css',)}
        js = ('js/forms/profile_password_change_form.js', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        """Check current password."""
        if not self.user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError(_('Invalid current password'))
        return self.cleaned_data['old_password']

    def clean_new_password2(self):
        """Validates new password."""
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']
        if password1 != password2:
            raise forms.ValidationError(_('Passwords are not equal'))
        return password2

    def save(self):
        """Change user password."""
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()
