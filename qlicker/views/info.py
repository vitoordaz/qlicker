import json

from django import http
from django import shortcuts

from qlicker.models import link
from qlicker.models import redirect


def info(unused_request, code):
    data = {}
    try:
        data['link'] = link.Link.objects.get(code=code)
    except link.Link.DoesNotExist:
        raise http.Http404()
    return shortcuts.render_to_response('info.html', data)


def info_clicks(request, code):
    try:
        l = link.Link.objects.get(code=code)
    except link.Link.DoesNotExist:
        return http.HttpResponseNotFound(json.dumps({'success': False,
                                                     'code': 'NotFound'}))

    # interval = (request.GET('interval') or '').lower()
    # if interval not in ('total', 'days', 'hourly'):
    #     return http.HttpResponseBadRequest(json.dumps({'success': False,
    #                                                    'code': 'BadRequest'}))

    data = l.to_json()
    data['stat'] = redirect.Redirect.objects.stat(link)
    return http.HttpResponse(json.dumps(data), content_type='application/json')
    # if not code:
    #     return rc('Link code required').BAD_REQUEST
    #
    # try:
    #     link = Links.objects.get(code=code)
    # except Links.DoesNotExist:
    #     return rc('Link does not exist').NOT_FOUND
    #
    # if interval == 'total':
    #     data = Redirects.objects.stat(type, link)
    # elif interval == 'days':
    #     try:
    #         days = int(req['days'])
    #     except KeyError:
    #         return rc('Days required').BAD_REQUEST
    #     except ValueError:
    #         return rc('Days must be integer').BAD_REQUEST
    #     if days not in (7, 14, 30):
    #         return rc('Wrong days').BAD_REQUEST
    #     data = Redirects.objects.stat(type, link, date.today() - timedelta(days=days))
    # elif interval == 'hourly':
    #     data = Redirects.objects.stat(type, link, datetime.now() - timedelta(hours=1), True)
    #
    # if type == 'clicks':
    #     res = []
    #     if interval == 'hourly':
    #         begin = datetime.now() - timedelta(minutes=60)
    #         t = datetime.now() - timedelta(minutes=59)
    #         while t < datetime.now():
    #             t += timedelta(minutes=1)
    #             res.append({'timestamp': int(time.mktime(t.timetuple())), 'clicks': 0})
    #         for i in data:
    #             res[(i['created_at'] - begin).seconds/60] = {'timestamp': int(time.mktime(i['created_at'].timetuple())), 'clicks': i['clicks']}
    #     else:
    #         begin = link.created_at.date()
    #         t = link.created_at.date()
    #         while t <= date.today():
    #             res.append({'timestamp': int(time.mktime(t.timetuple())), 'clicks': 0})
    #             t += timedelta(days=1)
    #         for i in data:
    #             res[(i['date'] - begin).days] = {'timestamp': int(time.mktime(i['date'].timetuple())), 'clicks': i['clicks']}
    #     data = res
    #
    # if type == 'clicks':
    #     cls = RedirectsClicksJSONEncoder
    # elif type == 'countries':
    #     cls = RedirectsCountriesJSONEncoder
    # elif type == 'domains':
    #     cls = RedirectsDomainsJSONEncoder
    # elif type == 'referrer':
    #     cls = RedirectsReferrerJSONEncoder
    #
    # res = {'code': 200, 'stat': 'ok', 'mes': 'ok', 'data': data}
    # return HttpResponse(json.dumps(res, cls=cls), mimetype='application/json')
