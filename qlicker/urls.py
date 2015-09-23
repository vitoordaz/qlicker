from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from qlicker.forms import password_reset
from qlicker.forms import set_password

from qlicker.views import activation
from qlicker.views import activation_abort
from qlicker.views import index
from qlicker.views import info
from qlicker.views import link
from qlicker.views import login
from qlicker.views import logout
from qlicker.views import password_change
from qlicker.views import password_reset as password_reset_view
from qlicker.views import profile
from qlicker.views import redirect
from qlicker.views import registration
from qlicker.views import registration_complete
from qlicker.views import registration_error


urlpatterns = [
    url(r'^admin/?', include(admin.site.urls)),

    url(r'^$', index.index, name='index'),
    url(r'^link/$', link.link, name='link'),
    url(r'^link/(?P<code>[0-9a-zA-Z]+)/stat$', link.link_stat,
        name='link_stat'),
    url(r'^register/$', registration.registration, name='registration'),
    url(r'^register/complete/$', registration_complete.registration_complete,
        name='registration_complete'),
    url(r'^register/error/$', registration_error.registration_error,
        name='registration_error'),
    url(r'^activate/abort/(?P<activation_key>\w+)',
        activation_abort.activation_abort, name='activation_abort'),
    url(r'^activate/(?P<activation_key>\w+)', activation.activation,
        name='activation'),
    url(r'^login/$', login.login, name='login'),
    url(r'^logout/$', logout.logout, {'next_page': '/'}, name='logout'),

    # password change
    url(r'^password/change/$', password_change.password_change,
        name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$', password_reset_view.password_reset, {
        'template_name': 'registration/password_reset.html',
        'password_reset_form': password_reset.PasswordResetForm
    }, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'set_password_form': set_password.SetPasswordForm},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),

    # profile
    url(r'^profile/?$', profile.profile, name='profile'),
    # url(r'^profile/password/change/$', views.password_change, name='profile_password_change'),
    # url(r'^profile/avatar/reset/$', views.avatar_reset, name='avatar_reset'),
    # url(r'^profile/avatar/load/$', views.avatar_load, name='avatar_load'),
    # url(r'^profile/twitter/$', views.twitter_make_access_token, name='twitter_make_access_token'),
    # url(r'^profile/twitter/get_link/$', views.twitter_get_auth_link, name='twitter_get_auth_link'),
    # url(r'^profile/fb/$', views.facebook, name='facebook'),
    # url(r'^profile/(?P<service>\w+)/remove/$', views.service_remove, name='service_remove'),
    # url(r'^profile/(?P<service>\w+)/toggle/$', views.service_toggle, name='service_toggle'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
    url(r'^(?P<code>[0-9a-zA-Z]+)$', redirect.redirect, name='redirect'),
    url(r'^(?P<code>[0-9a-zA-Z]+).info$', info.info, name='info'),
]
