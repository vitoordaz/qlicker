from django import forms
from django.utils.translation import gettext_lazy as _


class LoadAvatarForm(forms.Form):
    """User picture upload form."""

    avatar = forms.ImageField(
        label=_('User picture'), required=True,
        error_messages={'required': _('Image required'),
                        'invalid_image': _('Invalid image file')})

    class Media:
        css = {'all': ('css/forms/avatar_form.css',)}
        js = ('js/forms/avatar_form.js',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(LoadAvatarForm, self).__init__(*args, **kwargs)

    def save(self):
        self.user.avatar = self.cleaned_data['avatar']
        return self.user.save()
