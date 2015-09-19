#-*- coding: utf-8 -*-
'''
Created on 26.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.test import TestCase

from obrez.main.models import Links
from obrez.ouser.models import OUser

class LinksTest(TestCase):
    def setUp(self):
        self.user = OUser.objects.all()[0]
    
    def test_init(self):
        ''' Проверка нормализации ссылки в модели '''
        l = []
        l.append('http://qliker.ru/') 
        l.append('http://www.qliker.ru')
        l.append('qliker.ru')
        l.append('www.qliker.ru')
        
        for url in l:
            link = Links(url=url)
            self.assertEqual(link.url, l[0])
        
        l = []
        l.append('https://qliker.ru/')
        l.append('https://www.qliker.ru')

        for url in l:
            link = Links(url=url)
            self.assertEqual(link.url, l[0])
    
    def test_save(self):
        ''' Создание ссылок '''
        link = Links(url='http://www.pifopsfpgo12.ru/', user=self.user) #404
        link.save()
        self.assertEqual(link.title, 'Страница не найдена')
        
        # FIXME: Долго качается
        # слишком большой файл
        # link = Links(url='http://dev.mysql.com/get/Downloads/MySQL-5.1/mysql-5.1.56-osx10.6-x86_64.tar.gz/from/http://gd.tuwien.ac.at/db/mysql/')
        # link.save()
        # self.assertEqual(link.title, 'Страница не найдена')
        
        # FIXME: Долго качается
        # ссылка на маленький файл
        # link = Links(url='http://mysql.com/common/logos/logo-mysql-110x57.png')
        # link.save()
        # self.assertEqual(link.title, 'Страница не найдена')