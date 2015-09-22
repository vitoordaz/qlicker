from django.utils.translation import gettext_lazy as _
from django import http
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import models as auth_models
from django.contrib.auth import views


@csrf_protect
def password_reset(request, template_name, password_reset_form):
    if request.is_ajax() and request.method == 'GET':
        if 'email' in request.GET:
            user = auth_models.User.objects.filter(
                email__iexact=request.GET['email']).count()
            if user == 0:
                return http.HttpResponse(
                    _('User with a given email is not registered'), status=400)
            return http.HttpResponse('')
    return views.password_reset(request, template_name=template_name,
                                password_reset_form=password_reset_form)
