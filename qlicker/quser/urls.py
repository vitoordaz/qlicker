from django.conf.urls.defaults import url, patterns
from django.contrib.auth import views as auth_views

from qlicker.quser.forms import password_reset_form
# import forms
# import views


urlpatterns = patterns('',
    url(r'^register/$', views.registration, name='registration'),
    url(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    url(r'^register/error/$', views.registration_error, name='registration_error'),
    url(r'^activate/abort/(?P<activation_key>\w+)', views.activation_abort, name='activation_abort'),
    url(r'^activate/(?P<activation_key>\w+)', views.activation, name='activation'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),

    #password change
    url(r'^password/change/$', auth_views.password_change, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password/reset/$', views.password_reset, {'template_name': 'registration/password_reset.html',
        'password_reset_form': forms.PasswordResetForm}, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        {'set_password_form': forms.SetPasswordForm}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),

    # profile
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/password/change/$', views.password_change, name='profile_password_change'),
    url(r'^profile/avatar/reset/$', views.avatar_reset, name='avatar_reset'),
    url(r'^profile/avatar/load/$', views.avatar_load, name='avatar_load'),
    url(r'^profile/twitter/$', views.twitter_make_access_token, name='twitter_make_access_token'),
    url(r'^profile/twitter/get_link/$', views.twitter_get_auth_link, name='twitter_get_auth_link'),
    url(r'^profile/fb/$', views.facebook, name='facebook'),
    url(r'^profile/(?P<service>\w+)/remove/$', views.service_remove, name='service_remove'),
    url(r'^profile/(?P<service>\w+)/toggle/$', views.service_toggle, name='service_toggle'),
)
