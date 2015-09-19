#-*- coding: utf-8 -*-
'''
Created on 17.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

import json

from django.http import HttpResponse

class rc_factory(object):
    """
    Status codes.
    """
    CODES = dict(ALL_OK = ({'status': 'ok', 'code': 200}, 200),
                 CREATED = ({'status': 'ok', 'code': 201}, 201),
                 DELETED = ('', 204), # 204 says "Don't send a body!"
                 BAD_REQUEST = ({'status': 'fail', 'code': 400, 'mes': 'Bad Request'}, 400),
                 FORBIDDEN = ({'status': 'fail', 'code': 401, 'mes': 'Forbidden'}, 401),
                 NOT_FOUND = ({'status': 'fail', 'code': 404, 'mes': 'Not Found'}, 404),
                 DUPLICATE_ENTRY = ({'status': 'fail', 'code': 409, 'mes': 'Conflict/Duplicate'}, 409),
                 NOT_HERE = ({'status': 'fail', 'code': 410, 'mes': 'Gone'}, 410),
                 NOT_IMPLEMENTED = ({'status': 'fail', 'code': 501, 'mes': 'Not Implemented'}, 501),
                 THROTTLED = ({'status': 'fail', 'code': 503, 'mes': 'Throttled'}, 503))
    
    def __init__(self, mes=None):
        if mes:
            self.mes = mes
        
    def __getattr__(self, attr):
        """
        Returns a fresh `HttpResponse` when getting 
        an "attribute". This is backwards compatible
        with 0.2, which is important.
        """
        try:
            (r, c) = self.CODES.get(attr)
        except TypeError:
            raise AttributeError(attr)
        if r:
            if hasattr(self, 'mes'):
                if r['status'] == 'fail':
                    r['mes'] = self.mes
                elif r['status'] == 'ok':
                    r['data'] = self.mes  
            r = json.dumps(r)
        return HttpResponse(r, content_type='application/json', status=c)
    
rc = rc_factory
