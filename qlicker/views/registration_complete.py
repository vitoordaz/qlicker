from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django import http
from django.core.urlresolvers import reverse


def registration_complete(request):
    """Registration complete view."""
    if request.user.is_authenticated():
        return http.HttpResponseRedirect('/')
    if not request.session.get('registration_complete', None):
        return http.HttpResponseRedirect(reverse('registration'))
    del request.session['registration_complete']
    return render_to_response('registration/registration_complete.html', {},
                              context_instance=RequestContext(request))
