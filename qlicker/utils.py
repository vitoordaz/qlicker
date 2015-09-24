import boto
import datetime
import os
import tempfile
import threading
import urllib2
import uuid
import urlparse
import qrcode

import BeautifulSoup

from django.conf import settings


# Date for timestamp of the epoch.
EPOCH = datetime.datetime.utcfromtimestamp(0)


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


def datetime2timestamp(dv):
    if not dv:
        return
    if isinstance(dv, datetime.datetime):
        delta = dv - EPOCH
    else:
        delta = dv - EPOCH.date()
    millis = ((delta.days * 24 * 60 * 60 * 1000) +
              (delta.seconds * 1000) +
              (delta.microseconds / 1000))
    return millis


def create_qrcode(link):
    """This function generates QR code file for the given content."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(link.qlink)
    qr.make(fit=True)
    img = qr.make_image()
    fd, path = tempfile.mkstemp(prefix='qlicker-qr-')
    try:
        img.save(path)
    finally:
        os.close(fd)
    key_name = '%s.png' % uuid.uuid4().hex
    conn = boto.connect_s3()
    bucket = conn.create_bucket(settings.QR_CODES_BUCKET)
    key = bucket.new_key(key_name)
    headers = {'content-type': 'image/png'}
    key.set_contents_from_filename(path, headers=headers)
    key.make_public()
    link.qr_code = key.generate_url(expires_in=0, query_auth=False,
                                    force_http=True)
    link.save()


def get_link_meta(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        res = opener.open(link.url)
        encoding = None
        content_type = res.headers.get('Content-type', None)
        if content_type:
            charset_idx = content_type.find('charset=')
            if charset_idx:
                charset = content_type.strip()
                encoding = charset[charset_idx+len('charset='):]
        html = res.read(settings.MAX_FOR_DOWNLOAD)
        res.close()
        try:
            soup = BeautifulSoup.BeautifulSoup(
                html, fromEncoding=encoding,
                convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
            title = soup.find('title')
            if title:
                link.title = title.contents[0][:150]
            favicon = (soup.find('link', attrs={'rel': 'shortcut icon'}) or
                       soup.find('link', attrs={'rel': 'icon'}))
            if favicon:
                link.favicon = favicon.get('href', None)
        except TypeError:
            return
    except urllib2.URLError:
        return
    link.save()
    # get_favicon(favicon_url, link.url, '%s.png' % link.code)
    # if not link.user:
    #     link.save()
