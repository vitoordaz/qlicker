#-*- coding: utf-8 -*-
'''
Created on 12.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

import threading, os, urlparse, urllib2

from django.conf import settings

class QRCodeGen(threading.Thread):
    ''' Класс для генерации QR кодов '''
    def __init__(self, qrname):
        '''
        content -- информация которую нужно сохранить в qrcode
        file_name -- имя выходного файла
        '''
        self.file_name = os.path.join(settings.QRCODE_DIR, qrname)
        self.content = urlparse.urljoin(settings.SITE_URL, qrname)
        super(QRCodeGen, self).__init__()

    def run(self):
        try:
            import qrcode
            qrc = qrcode.Encoder()
            img = qrc.encode(self.content,
                             width=settings.QRCODE_WIDTH,
                             version=settings.QRCODE_VERSION,
                             mode=qrc.mode.ALNUM,
                             eclevel=qrc.eclevel.H)
            img.save(self.filename, 'png')
        except ImportError:
            print "Error: require qrcode module"

class GetLinkMeta(threading.Thread):
    ''' Класс для получение загаловка и иконки страницы '''
    def __init__(self, instance):
        self.inst = instance
        super(GetLinkMeta, self).__init__()
    def run(self):
        try:
            res = urllib2.urlopen(self.inst.url)
        except urllib2.URLError:
            print "What to do?"
        self.inst.save()


def add_link_meta(instance, **kwargs):
    ''' Функция для сбора дополнительной информации о ссылке '''
    if instance.code:
        #генерирую qrcode
        qr = QRCodeGen("%s.qr" % instance.code)
        qr.start()
        #получения загаловка и иконки страницы
        meta = GetLinkMeta(instance)
        meta.start()
        print instance.id, instance, instance.code