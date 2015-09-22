import re

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from qlicker import utils
from qlicker.main.models import link


URL_PATTERN = re.compile(r'(:?http://|https://)?'
                         r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
                         r'[A-Z]{2,6}\.?/?'
                         r'(?:/?[A-Z0-9-_\.\?=\+%&#!:]/?)*', re.IGNORECASE)

QLINK_PATTERN = re.compile(
    r'^(http://)?(www\.)?%s/[a-zA-Z0-9]{1,6}$' % settings.HOSTNAME,
    re.IGNORECASE)


class AddLinkForm(forms.Form):

    url = forms.URLField(required=True, error_messages={
        'required': _('Link required'),
        'invalid': _('Input a valid link'),
        'invalid_link': _('Referenced resource does not exist')})

    def clean_url(self):
        url = self.cleaned_data.get('url', None)
        if url:
            url = utils.normalize_url(url)
            if re.match(QLINK_PATTERN, url):
                raise forms.ValidationError(_('This link is already Qlink'))
            return url

    def save(self):
        return link.Link.objects.get_or_create(url=self.cleaned_data['url'],
                                               user=None)[0]
