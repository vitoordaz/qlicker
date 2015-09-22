from django.template.context import RequestContext
from django import http
from django import shortcuts

from qlicker.models import registration_profile


RegistrationProfile = registration_profile.RegistrationProfile


def activation_abort(request, activation_key):
    """Aborts registration."""
    if request.user.is_authenticated():
        return http.HttpResponseRedirect('/')
    if not RegistrationProfile.objects.abort_activation(activation_key):
        return shortcuts.render_to_response(
            'registration/activation_abort_fail.html', {},
            context_instance=RequestContext(request))
    return shortcuts.render_to_response(
        'registration/activation_abort.html', {},
        context_instance=RequestContext(request))
