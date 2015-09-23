import json
import os

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

from qlicker.forms import login as login_form
from qlicker.forms import add_link as add_link_form
from qlicker.models import link as link_model


def index(request):
    if request.user.is_anonymous():
        return index_anonymous(request)
    return index_authenticated(request)


@decorators.login_required
def index_authenticated(request):
    """Index page for authenticated users."""
    data = {}
    try:
        page = int(request.GET.get('p', '1'))
    except ValueError:
        page = 1
    if request.method == 'POST':
        if request.POST.get('share', None):
            operation = 'share'
        elif request.POST.get('short', None):
            operation = 'short'
        form = add_link_form.AddLinkFormAuthenticated(operation, request.POST)
        if form.is_valid():
            result = form.save(request.user)
            data.update(result)
        elif request.is_ajax():
            return HttpResponse(json.dumps({'error': form.errors}),
                                mimetype=r'application/json')
    else:
        form = add_link_form.AddLinkFormAuthenticated()
    p = Paginator(link_model.Link.objects.for_user(request.user), 10)
    try:
        links = p.page(page)
    except (EmptyPage, InvalidPage):
        links = p.page(p.num_pages)
    if request.is_ajax():
        data['links'] = [{
            'url': l.long,
            'code': l.code,
            'title': l.title,
            'date': l.created_at.isoformat(),
            'favicon': l.favicon,
            'qlink': l.qlink,
            'counter': l.counter
        } for l in links.object_list]
        data['pages'] = {
            'previous': links.previous_page_number(),
            'current': links.number,
            'next': links.next_page_number(),
            'last': links.paginator.num_pages
        }
        return HttpResponse(json.dumps(data), mimetype=r'application/json')
    c = {
        'form': form,
        'links': links
        # 'services': request.user.services,
        # 'active_services': request.user.active_services
    }
    return render_to_response('index_authenticated.html', c,
                              context_instance=RequestContext(request))


def index_anonymous(request):
    """Index page for anonymous users."""
    if request.method == 'GET':
        form = add_link_form.AddLinkForm()
    else:
        form = add_link_form.AddLinkForm(request.POST)
        if not form.is_valid():
            if request.is_ajax():
                return HttpResponse(json.dumps({'error': form.errors}),
                                    status=400, mimetype=r'application/json')
        else:
            l = form.save()
            t = request.session.get('links', [])
            if l not in t:
                t.insert(0, l)
                request.session['links'] = t

    p = Paginator(request.session.get('links', []), 10)
    try:
        page = int(request.GET.get('p', '1'))
    except ValueError:
        page = 1
    try:
        links = p.page(page)
    except (EmptyPage, InvalidPage):
        links = p.page(p.num_pages)

    if request.is_ajax():
        data = {}
        if request.method == 'POST':
            data['link'] = {'url': l.long, 'code': l.code}
        else:
            data['links'] = [{'url': l.long, 'code': l.code}
                             for l in links.object_list]
        data['pages'] = {'previous': links.previous_page_number(),
                         'current': links.number,
                         'next': links.next_page_number(),
                         'last': links.paginator.num_pages}
        return HttpResponse(json.dumps(data), mimetype=r'application/json')

    c = {'form': form, 'auth_form': login_form.LoginForm(), 'links': links}
    return render_to_response('index_anonymous.html', c,
                              context_instance=RequestContext(request))


@csrf_protect
@decorators.login_required
def edit_title(request, code):
    """Edit link title view."""
    if request.method == 'POST' and request.is_ajax():
        title = request.POST.get('title', None)
        if title:
            try:
                link = link_model.Link.objects.for_user(request.user).get(
                    code=code)
                link.set_title(title)
                link.save()
                return HttpResponse('edited')
            except:
                pass
        return HttpResponse('not edited')
    return HttpResponseRedirect(reverse('index'))


def qrcode(request, code):
    """QR code view."""
    filename = os.path.join(settings.QRCODE_DIR, "%s.qr" % code)
    if os.path.exists(filename):
        f = open(filename)
        return HttpResponse(f.read(), content_type='image/png')
