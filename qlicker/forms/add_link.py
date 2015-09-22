import re

from django import forms
from django.utils.translation import gettext_lazy as _

from qlicker import utils
from qlicker.models import link as link_model


URL_PATTERN = re.compile(r'(:?http://|https://)?'
                         r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
                         r'[A-Z]{2,6}\.?/?'
                         r'(?:/?[A-Z0-9-_\.\?=\+%&#!:]/?)*', re.IGNORECASE)

QLINK_PATTERN = re.compile(r'^(http://)?(www\.)?qliker.ru/[a-zA-Z0-9]{1,6}$',
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
        return link_model.Link.objects.get_or_create(
            url=self.cleaned_data['url'], user=None)[0]


class AddLinkFormAuthenticated(forms.Form):
    url = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'cols': 65,
            'rows': 3,
            'autocomplete': 'off'}))

    class Media:
        css = {'all': ('css/forms/add_link_form_authenticated.css',)}

    def __init__(self, operation=None, *args, **kwargs):
        self.operation = operation
        super(AddLinkFormAuthenticated, self).__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if self.operation == 'short':
            if url == '':
                raise forms.ValidationError(_('URL required'))
            elif not re.findall(URL_PATTERN, url):
                raise forms.ValidationError(_('Invalid URL'))
            elif re.match(QLINK_PATTERN, self.cleaned_data['url']):
                raise forms.ValidationError(_('Already qlink'))
        elif self.operation == 'share':
            if url == '':
                raise forms.ValidationError(_('Message required'))
        return url

    def save(self, user):
        match = URL_PATTERN.finditer(self.cleaned_data['url'])
        msg = self.cleaned_data['url']
        objects = {'added': []}
        for url in match:
            normalized_url = utils.normalize_url(url.group())
            if not QLINK_PATTERN.match(normalized_url):
                obj, created = link_model.Link.objects.get_or_create(
                    url=normalized_url, user=user)
                obj.recover()
                obj.updated_now()
                obj.save()
                objects['added'].append({
                    'code': obj.code,
                    'qlink': obj.qlink,
                    'url': url.group()
                })
                msg = msg.replace(url.group(), obj.qlink)
        if self.operation == 'share':
            objects['status'] = user.update_status(msg)
        return objects
