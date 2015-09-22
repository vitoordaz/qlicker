from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from qlicker.models import registration_profile


RegistrationProfile = registration_profile.RegistrationProfile


def activation(request, activation_key):
    """User activation view."""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not RegistrationProfile.objects.activate_user(activation_key):
        return render_to_response('registration/activation_fail.html', {},
                                  context_instance=RequestContext(request))
    return render_to_response('registration/activation.html', {},
                              context_instance=RequestContext(request))
