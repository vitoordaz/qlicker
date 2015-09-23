import json

from django import http

from qlicker.forms import add_link as add_link_form

from qlicker.models import link as link_model
from qlicker.models import redirect


def link(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = add_link_form.AddLinkForm(data)
        if not form.is_valid():
            data = {'success': False, 'errors': form.errors}
            return http.HttpResponse(json.dumps(data), status=400,
                                     content_type='application/json')
        l = form.save()
        links = request.session.get('links', [])
        obj = l.to_json()
        if obj not in links:
            links.insert(0, obj)
            request.session['links'] = links
        return http.HttpResponse(json.dumps({'success': True}), status=201,
                                 content_type='application/json')
    elif request.method == 'GET':
        links = request.session.get('links', [])
        data = {
            'success': True,
            'meta': {'total': len(links)},
            'data': links
        }
        return http.HttpResponse(json.dumps(data),
                                 content_type='application/json')
    return http.HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def link_stat(request, code):
    if request.method == 'GET':
        try:
            l = link_model.Link.objects.get(code=code)
        except link_model.Link.DoesNotExist:
            return http.HttpResponseNotFound(json.dumps({
                'success': False,
                'code': 'NotFound'
            }))
        data = redirect.Redirect.objects.stat(l)
        return http.HttpResponse(json.dumps(data),
                                 content_type='application/json')
    return http.HttpResponseNotAllowed(permitted_methods=['GET'])
