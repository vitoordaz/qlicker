from django.contrib.auth import decorators
from django.template import context
from django.shortcuts import render_to_response

from qlicker.forms import password_change
from qlicker.forms import load_avatar


@decorators.login_required
def profile(request, action=''):
    """User profile view."""
    c = {}
    if request.method == 'POST':
        if action == 'password_change':
            c['ch_pswd_form'] = password_change.PasswordChangeForm(request.user,
                                                                   request.POST)
        else:
            c['ch_pswd_form'] = password_change.PasswordChangeForm(request.user)
        if not request.user.avatar:
            if action == 'avatar_load':
                c['avatar_form'] = load_avatar.LoadAvatarForm(
                    request.user, request.POST, request.FILES)
            else:
                c['avatar_form'] = load_avatar.LoadAvatarForm(request.user)
    else:
        c['services'] = request.user.services
        c['ch_pswd_form'] = password_change.PasswordChangeForm(request.user)
        if not request.user.avatar:
            c['avatar_form'] = load_avatar.LoadAvatarForm(request.user)
    return render_to_response('registration/profile.html', c,
                              context_instance=context.RequestContext(request))
