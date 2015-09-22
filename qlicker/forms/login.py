from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class LoginForm(AuthenticationForm):
    """User login form."""

    username = forms.SlugField(label=_('Username:'),
                               widget=forms.TextInput(attrs={'class': 'text'}),
                               max_length=30,
                               error_messages={'required': _('Input username')})

    password = forms.CharField(
        label=_('Password:'),
        widget=forms.PasswordInput(attrs={'class': 'text'}),
        error_messages={'required': _('Input password')})

    class Media:
        css =  {'all': ('css/forms/login_form.css',)}
        js = ('js/forms/login_form.js', )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username and not password:
            raise forms.ValidationError(_('Input username and password'))

        self.user_cache = authenticate(username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError(_('Input valid username and password'))
        elif not self.user_cache.is_active:
            raise forms.ValidationError(_('User account is not active'))

        super(LoginForm, self).clean()
