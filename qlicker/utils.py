import string
import os
import cStringIO
import shutil
import threading
import urlparse
import urllib2
import urllib

from django.conf import settings
from django.template.defaultfilters import stringfilter

from PIL import Image

import BeautifulSoup as bs


def download_service_avatar(filename, url):
    u = urllib2.urlopen(url)
    if os.path.exists(filename):
        os.remove(filename)
    img = open(filename, 'wb')
    img.write(u.read())
    img.close()
    u.close()


class AvatarLoader(threading.Thread):

    def __init__(self, filename, url):
        super(AvatarLoader, self).__init__()
        self.filename = filename
        self.url = url

    def run(self):
        download_service_avatar(self.filename, self.url)


def normalize_url(url):
    """This function normalizes given url."""
    url = list(urlparse.urlsplit(url))
    if not url[0]: # if protocol is not given, we can assume http
        url[0] = 'http'
    if not url[1]:
        del url[1]
        url.append('')
    if url[1].startswith('www.'):  # remove www.
        url[1] = url[1].replace('www.', '', 1)
    if not url[2]:
        url[2] = '/'
    return urlparse.urlunsplit(url)


def get_favicon(favicon_url, link, filename):
    """This function downloads favicon.

    :param favicon_url favicon URL.
    :param link link URL.
    :param filename filename for a new favicon.
    """
    if not favicon_url:
        # If favicon_url is not given we can assume that favicon is in root.
        fav_url_obj = list(urlparse.urlsplit(link))
        fav_url_obj[2] = '/favicon.ico'
    else:
        fav_url_obj = list(urlparse.urlsplit(favicon_url))
        if not fav_url_obj[0]: # scheme is not given -> use http
            fav_url_obj[0] = 'http'
        if not fav_url_obj[1]: # domain is not available -> use link domain
            link_url_obj = list(urlparse.urlsplit(link))
            fav_url_obj[1] = link_url_obj[1]
    favicon_url = urlparse.urlunsplit(fav_url_obj)
    filename = os.path.join(settings.FAVICON_ROOT, filename)
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        resp = opener.open(favicon_url)
        img_src = cStringIO.StringIO(resp.read(settings.MAX_FOR_DOWNLOAD))
        with Image.open(img_src):
          with open(filename, 'wb') as fp:
            fp.write(img_src.getvalue())
    except:
        shutil.copy2(settings.STANDART_FAVICON, filename)


def encode(d):
    """Converts number to base 62 representation."""
    if not d:
        return str(0)
    base = 62   # 0-9 + a-z + A-Z = 62
    val = []
    while d:
        rem = d % base
        val.insert(0, get_symbol(rem))
        d /= base
    return ''.join(val)


def get_symbol(c):
    """Returns symbol for a number in 62 base."""
    if 36 <= c < 62:
        return chr(ord('A') + c - 36)
    elif 10 <= c < 36:
        return chr(ord('a') + c - 10)
    return str(c)


@stringfilter
def unquote(value):
    return urllib.unquote(value)


def gen_qrcode(filename, content):
    '''
    Функция для генерации QR кодов
    qrname -- имя выходного файла
    '''
    try:
        from qrencode import Encoder
        qrc = Encoder()
        img = qrc.encode(content, {'width': settings.QRCODE_WIDTH})
        img.save(filename, 'png')
        return True
    except ImportError:
        print 'Error: require qrencode module'
        return False


class QRCodeGen(threading.Thread):
    ''' Класс для генерации QR кодов '''
    def __init__(self, qrname):
        ''' qrname -- имя выходного файла '''
        self.filename = os.path.join(settings.QRCODE_DIR, "%s.qr" % qrname)
        self.content = urlparse.urljoin(settings.SITE_URL, qrname) + '?qr'
        super(QRCodeGen, self).__init__()

    def run(self):
        return gen_qrcode(self.filename, self.content)


def get_link_meta(link):
    '''
    Функция для сбора мета информации со страницы
    link -- объект моделии Links
    '''
    favicon_url = None
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        res = opener.open(link.url)
        # определяем кодировку страницы
        encoding = None
        content_type = res.headers.get('Content-type', None)
        if content_type:
            charset_ind = content_type.find('charset=')
            if charset_ind:
                charset = string.strip(content_type)
                encoding = charset[charset_ind+len('charset='):]
        html = res.read(settings.MAX_FOR_DOWNLOAD)
        res.close()
        try:
            soup = bs.BeautifulSoup(html,
                                    fromEncoding=encoding,
                                    convertEntities=bs.BeautifulStoneSoup.HTML_ENTITIES)
            # title
            title = soup.find('title')
            if title:
                link.title = title.contents[0][:150]
            # favicon
            favicon = soup.find('link', attrs={'rel': 'shortcut icon'}) or soup.find('link', attrs={'rel': 'icon'})
            if favicon:
                favicon_url = favicon.get('href', None)
        except TypeError:  # поврежденный документ или не html
            link.title = link.url
    except urllib2.URLError:# страница не найдена
        link.title = 'Страница не найдена'
    get_favicon(favicon_url, link.url, '%s.png' % link.code)
    if not link.user: # функция запущена в отдельном потоке
        link.save()


# class UpdateTwitterStatus(threading.Thread):
#     ''' Класс потока для обновления статуса в twiiter '''
#     def __init__(self, msg, user):
#         self.msg = msg
#         self.user = user
#         super(UpdateTwitterStatus, self).__init__()
#
#     def run(self):
#         try:
#             tw_account = Twitter.objects.get(ouser=self.user)
#             if tw_account.active:
#                 tw = oauthtwitter.OAuthApi(settings.TWITTER_CONSUMER_KEY,
#                                            settings.TWITTER_CONSUMER_SECRET,
#                                            tw_account.oauth_token,
#                                            tw_account.oauth_token_secret)
#                 tw.UpdateStatus(self.msg.encode('utf-8'))
#         except urllib2.HTTPError:
#             print "Can't update"
#         except Twitter.DoesNotExist:
#             print "User don't have twitter account"
#
#
# class UpdateFacebookStatus(threading.Thread):
#     ''' Класс потока для обновления статуса в facebook '''
#     def __init__(self, msg, user):
#         self.msg = msg
#         self.user = user
#         super(UpdateFacebookStatus, self).__init__()
#
#     def run(self):
#         try:
#             fb_account = Facebook.objects.get(ouser=self.user)
#             if fb_account.active:
#                 fb = oauthfacebook.OAuthApi(access_token=fb_account.access_token)
#                 fb.updateStatus(self.msg.encode('utf-8'))
#         except Facebook.DoesNotExist:
#             print "User don't have facebook account"
