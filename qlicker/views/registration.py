from django.utils.translation import gettext_lazy as _
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django import http
from django.contrib.auth import models
from django.core.urlresolvers import reverse

from qlicker.forms import registration as registration_form


def registration(request):
    """Registration view."""
    if request.user.is_authenticated():
        return http.HttpResponseRedirect('/')
    if request.is_ajax():
        if request.method == 'GET':
            if 'username' in request.GET:
                try:
                    models.User.objects.get(username=request.GET['username'])
                    return http.HttpResponse(
                        _(u'User with a given username already exist'),
                        status=400)
                except models.User.DoesNotExist:
                    return http.HttpResponse()
            if 'email' in request.GET:
                try:
                    models.User.objects.get(email=request.GET['email'])
                    return http.HttpResponse(_(u'Given email is already used'),
                                             status=400)
                except models.User.DoesNotExist:
                    return http.HttpResponse()
    if request.method == 'POST':
        form = registration_form.RegistrationForm(request.POST)
        if form.is_valid():
            if form.save():  # registration successful
                request.session['registration_complete'] = True
                return http.HttpResponseRedirect(
                    reverse('registration_complete'))
            request.session['registration_fail'] = True
            return http.HttpResponseRedirect(reverse('registration_error'))
    else:
        form = registration_form.RegistrationForm()
    return render_to_response('registration/registration.html', {'form': form},
                              context_instance=RequestContext(request))
