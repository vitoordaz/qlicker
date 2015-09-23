import datetime
import os
import threading
import urllib2
import urlparse


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
