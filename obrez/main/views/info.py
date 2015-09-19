#-*- coding: utf-8 -*-
'''
Created on 22.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
import time, json
from datetime import date, timedelta, datetime

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from main.models import Links, Redirects
from main.models.redirect import RedirectsClicksJSONEncoder, RedirectsCountriesJSONEncoder, RedirectsDomainsJSONEncoder, RedirectsReferrerJSONEncoder
from main.utils import rc

def info(request, code):
    '''
    Статистика по ссылке.
    '''
    try:
        link = Links.objects.get(code=code)
    except Links.DoesNotExist:
        raise Http404
    return render_to_response('info.html', {'link': link},
                              context_instance=RequestContext(request))
    
def info_clicks(request, type, interval):
    ''' 
    Статистика по кликам
        type:
            clicks -- статистика по кликам
            countries -- статистика по странам перехода
            domains -- статистика по источникам перехода (домены)
            referrer -- статистика по источникам перехода (домены и путь) 
        interval:
            total -- за весь период
            days -- за days в POST
            hourly -- за последний час
    '''
    req = request.GET
    code = req.get('code', None)
    
    if not code:
        return rc('Link code required').BAD_REQUEST
    
    try:
        link = Links.objects.get(code=code)
    except Links.DoesNotExist:
        return rc('Link does not exist').NOT_FOUND
    
    if interval == 'total':
        data = Redirects.objects.stat(type, link)
    elif interval == 'days':
        try:
            days = int(req['days'])
        except KeyError:
            return rc('Days required').BAD_REQUEST
        except ValueError:
            return rc('Days must be integer').BAD_REQUEST
        if days not in (7, 14, 30):
            return rc('Wrong days').BAD_REQUEST
        data = Redirects.objects.stat(type, link, date.today() - timedelta(days=days))
    elif interval == 'hourly':
        data = Redirects.objects.stat(type, link, datetime.now() - timedelta(hours=1), True)
    
    if type == 'clicks':
        res = []
        if interval == 'hourly':
            begin = datetime.now() - timedelta(minutes=60)
            t = datetime.now() - timedelta(minutes=59)
            while t < datetime.now():
                t += timedelta(minutes=1)
                res.append({'timestamp': int(time.mktime(t.timetuple())), 'clicks': 0})
            for i in data:
                res[(i['created_at'] - begin).seconds/60] = {'timestamp': int(time.mktime(i['created_at'].timetuple())), 'clicks': i['clicks']}
        else:
            begin = link.created_at.date()
            t = link.created_at.date()
            while t <= date.today():
                res.append({'timestamp': int(time.mktime(t.timetuple())), 'clicks': 0})
                t += timedelta(days=1)
            for i in data:
                res[(i['date'] - begin).days] = {'timestamp': int(time.mktime(i['date'].timetuple())), 'clicks': i['clicks']}
        data = res
        
    if type == 'clicks':
        cls = RedirectsClicksJSONEncoder
    elif type == 'countries':
        cls = RedirectsCountriesJSONEncoder
    elif type == 'domains':
        cls = RedirectsDomainsJSONEncoder
    elif type == 'referrer':
        cls = RedirectsReferrerJSONEncoder
        
    res = {'code': 200, 'stat': 'ok', 'mes': 'ok', 'data': data}
    return HttpResponse(json.dumps(res, cls=cls), mimetype='application/json')