import os
import urllib2
import threading


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
