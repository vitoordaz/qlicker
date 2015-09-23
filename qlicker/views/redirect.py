import threading

from django import http

from qlicker.models import link
from qlicker.models import redirect as redirect_model


def redirect(request, code):
    try:
        l = link.Link.objects.get(code=code)
        threading.Thread(target=redirect_model.create_redirect,
                         args=[l, request]).start()
        return http.HttpResponseRedirect(l.url)
    except link.Link.DoesNotExist:
        raise http.Http404()
