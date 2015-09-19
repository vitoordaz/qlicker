#-*- coding: utf-8 -*-
'''
Created on 26.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.utils.translation import gettext_lazy as _
from django.test import TestCase

from obrez.main.fun import encode, QRCodeGen, norm_url

class encodeTest(TestCase):
    ''' Проверка функции encode '''
    def test_success(self):
        # крайние точки
        self.assertEqual(encode(0), '0')
        self.assertEqual(encode(10), 'a')
        self.assertEqual(encode(35), 'z')
        self.assertEqual(encode(36), 'A')
        self.assertEqual(encode(61), 'Z')
        # серидина
        self.assertEqual(encode(62), '10')
        self.assertEqual(encode(63), '11')
        self.assertEqual(encode(72), '1a')

class norm_urlTest(TestCase):
    ''' Проверка функции нормализации url norm_url '''
    def test_success(self):
        l = []
        l.append('http://qliker.ru/') # правильная ссылка
        l.append('qliker.ru')
        l.append('www.qliker.ru')
        l.append('http://www.qliker.ru')
        for i in l:
            self.assertEqual(norm_url(i), l[0])
        
class QRCodeGenTest(TestCase):
    ''' Проверка генератора qr кодов '''
    def test_success(self):
        try:
            import qrencode,  os
            t = QRCodeGen('test')
            self.assertEqual(t.content, 'http://qliker.ru/test?qr') # содержимое qr кода правильно
            self.assertTrue(t.run()) # qr код сгенерирован
            self.assertTrue(os.path.exists(t.filename))
            os.remove(t.filename)
        except ImportError:
            raise AssertionError('Error require qrencode module')