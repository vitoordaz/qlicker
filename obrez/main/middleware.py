'''
Created on 12.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

import sys, cProfile
from cStringIO import StringIO

from django.conf import settings

class ProfilerMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler.create_stats()
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
            self.profiler.print_stats(1)
            sys.stdout = old_stdout
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response

class SetRemoteAddrFromForwardedFor(object):
        """
        Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
        latter is set. This is useful if you're sitting behind a reverse proxy that
        causes each request's REMOTE_ADDR to be set to 127.0.0.1.
    
        Note that this does NOT validate HTTP_X_FORWARDED_FOR. If you're not behind
        a reverse proxy that sets HTTP_X_FORWARDED_FOR automatically, do not use
        this middleware. Anybody can spoof the value of HTTP_X_FORWARDED_FOR, and
        because this sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, that means
        anybody can "fake" their IP address. Only use this when you can absolutely
        trust the value of HTTP_X_FORWARDED_FOR.
        """
        def process_request(self, request):
            try:
                real_ip = request.META['HTTP_X_REAL_IP']
            except KeyError:
                return None
            else:
                # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
                # client's IP will be the first one.
                real_ip = real_ip.split(",")[0].strip()
                request.META['REMOTE_ADDR'] = real_ip