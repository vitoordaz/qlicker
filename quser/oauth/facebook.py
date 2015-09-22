import json
import urllib
import urllib2


# Taken from http://developers.facebook.com/docs/authentication/
ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
AUTHORIZATION_URL = 'https://www.facebook.com/dialog/oauth'


class OAuthApi():
    def __init__(self, **kwargs):
        self.client_id = kwargs.get('client_id', None)
        self.client_secret = kwargs.get('client_secret', None)
        self.code = kwargs.get('code', None)
        self.access_token = kwargs.get('access_token', None)

    def _GetOpener(self):
        return urllib2.build_opener()

    def _FetchUrl(self, url, http_method=None, parameters=None):
        opener = self._GetOpener()

        if parameters is None:
          parameters = {}

        parameters['access_token'] = self.access_token
        params = urllib.urlencode(parameters)
        if  http_method == 'GET':
            url_data = opener.open('%s?%s' % (url, params)).read()
        else:
            url_data = opener.open(url, params).read()
        opener.close()
        return url_data

    def getAuthorizationURL(self, redirect_uri, scope, url=AUTHORIZATION_URL):
        return "%s?%s" % (url, urllib.urlencode({'client_id': self.client_id,
                                                 'redirect_uri': redirect_uri,
                                                 'scope': scope}))

    def getAccessToken(self, redirect_uri, url=ACCESS_TOKEN_URL):
        params = urllib.urlencode({'client_id': self.client_id,
                                   'redirect_uri': redirect_uri,
                                   'client_secret': self.client_secret,
                                   'code': self.code})
        opener = self._GetOpener()
        self.access_token = opener.open("%s?%s" % (url, params)).read()
        opener.close()
        if self.access_token.startswith('access_token='):
            self.access_token = self.access_token[len('access_token='):]
        return self.access_token

    def getUser(self):
        return self.ApiCall('me')

    def getAccounts(self):
        """Returns a list of accounts.

        GET https://graph.facebook.com/me/accounts
        """
        return self.ApiCall('me/accounts')

    def getPicture(self, type):
        """Returns user picture.

        GET https://graph.facebook.com/me/picture
        """
        url = ('https://graph.facebook.com/me/picture?access_token=%(token)s&'
               'type=%(type)s')
        return url % {'token': self.access_token, 'type': type or 'normal'}

    def UpdateStatus(self, message, user_id=None):
        """Updates user status (feed).

        POST https://graph.facebook.com/me/feed or
        POST https://graph.facebook.com/<id>/feed
        """
        url = '%s/feed' % user_id if user_id else 'me/feed'
        return self.ApiCall(url, 'POST', {'message': message})

    def ApiCall(self, path, method='GET', parameters=None):
        try:
            url = 'https://graph.facebook.com/%s' % path
            json_str = self._FetchUrl(url, method, parameters or {})
            return json.loads(json_str)
        except urllib2.HTTPError:
            return {}
