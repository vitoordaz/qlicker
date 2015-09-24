from django import http
from django import shortcuts
from django.template import context

from qlicker.models import link


def info(request, code):
    data = {}
    try:
        data['link'] = link.Link.objects.get(code=code)
    except link.Link.DoesNotExist:
        raise http.Http404()
    return shortcuts.render_to_response(
        'info.html', data, context_instance=context.RequestContext(request))
