import json

from django import http

from qlicker.forms import add_link as add_link_form


def link(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = add_link_form.AddLinkForm(data)
        if not form.is_valid():
            data = {'success': False, 'errors': form.errors}
            return http.HttpResponse(json.dumps(data), status=400,
                                     content_type=r'application/json')
        l = form.save()
        links = request.session.get('links', [])
        obj = l.to_json()
        if obj not in links:
            links.insert(0, obj)
            request.session['links'] = links
        return http.HttpResponse(status=201)
    elif request.method == 'GET':
        links = request.session.get('links', [])
        data = {
            'success': True,
            'meta': {'total': len(links)},
            'data': links
        }
        return http.HttpResponse(json.dumps(data),
                                 content_type=r'application/json')
    return http.HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
