# Library modules
import urllib, urllib2, json

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
        opener = urllib2.build_opener()
        return opener

    def _FetchUrl(self, url, http_method=None, parameters={}):
        opener = self._GetOpener()

        parameters['access_token'] = self.access_token
        params = urllib.urlencode(parameters)
        if  http_method == 'GET':
            url_data = opener.open(url+'?'+params).read()
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
        return self.ApiCall("me")

    def getAccounts(self):
        ''' https://graph.facebook.com/me/accounts?access_token=TOKEN_FROM_ABOVE '''
        return self.ApiCall('me/accounts')
    
    def getPicture(self, type):
        ''' https://graph.facebook.com/me/picture?access_token=ACCESS_TOKEN?type=normal '''
        return 'https://graph.facebook.com/me/picture?access_token=%s&type=%s' % (self.access_token, type or 'normal')

    def UpdateStatus(self, message, id=None):
        ''' https://graph.facebook.com/me/feed or https://graph.facebook.com/ID/feed '''
        if id:
            return self.ApiCall('%s/feed' % id, 'POST', {'message': message})
        return self.ApiCall('me/feed', 'POST', {'message': message})
    
    def ApiCall(self, call, type="GET", parameters={}):
        try:
            json_str = self._FetchUrl(u"https://graph.facebook.com/" + call, type, parameters)
            return json.loads(json_str)
        except urllib2.HTTPError:# HTTP 404 (Bad request)
            return {}