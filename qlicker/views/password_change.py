import json

from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from qlicker.forms import password_change as password_change_form
from qlicker.views import profile as profile_view


@login_required
def password_change(request):
    """Password change view."""
    if request.method == 'POST':
        form = password_change_form.PasswordChangeForm(request.user,
                                                      request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return http.HttpResponse()
            return http.HttpResponseRedirect(reverse('profile'))
        if request.is_ajax():
            return http.HttpResponse(json.dumps({'error': form.errors}))
        return profile_view.profile(request, 'password_change')
    return http.HttpResponseRedirect(reverse('profile'))
