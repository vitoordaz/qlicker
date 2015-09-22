from django import http
from django.contrib.auth import views


def logout(request, next_page):
    """User logout view."""
    if request.user.is_authenticated():
        return views.logout(request, next_page=next_page)
    return http.HttpResponseRedirect(next_page)
