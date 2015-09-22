from django import http
from django.contrib.auth import views

from qlicker.forms import login as login_form


def login(request):
    """User login view."""
    if request.user.is_authenticated():
        return http.HttpResponseRedirect('/')
    return views.login(request, authentication_form=login_form.LoginForm,
                       template_name='registration/login.html')
