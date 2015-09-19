#-*- coding: utf-8 -*-
'''
Created on 26.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from obrez.main.models import Links, Redirects

class TestIndexAnonymous(TestCase):
    def setUp(self):
        self.c = Client()
        Links.objects.all().delete()
    
    def test_simple(self):
        ''' Проверка загрузки правильного шаблона '''
        r = self.c.get(reverse('index'))
        self.assertTemplateUsed(r, 'index_anonymous.html')
        self.assertTemplateNotUsed(r, 'index_authenticated.html')
        
    def test_add_link(self):
        ''' Проверка добавления ссылки '''
        r = self.c.post(reverse('index'), {'url': 'http://yandex.ru'})
        self.assertNotEqual(r.context['links'].object_list, {}) # ссылка добавлена
        self.assertNotEqual(self.c.session['links'], {}) # ссылка добавленна в сессию
        # добавляем ссылку повторно
        r = self.c.post(reverse('index'), {'url': 'http://yandex.ru'})
        self.assertEqual(len(r.context['links'].object_list), 1) # ссылка уже есть
        self.assertEqual(len(self.c.session['links']), 1) # ссылка уже есть
        self.setUp()
        
    def test_add_link_ajax(self):
        ''' Проверка добаления ссылок (ajax запрос) '''
        r = self.c.post(reverse('index'), {'url': 'http://yandex.ru'},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.content, '{"link": {"url": "http://yandex.ru/", "code": "3"}, '
                                    '"pages": {"current": 1, "next": 2, "last": 1, "previous": 0}}')
        
        r = self.c.post(reverse('index'), {'url': 'http://yandex.ru'}, # ссылка уже есть
                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.content, '{"link": {"url": "http://yandex.ru/", "code": "3"}, '
                                    '"pages": {"current": 1, "next": 2, "last": 1, "previous": 0}}')
        
class TestRedirect(TestCase):
    def setUp(self):
        self.c = Client()
        self.l, created = Links.objects.get_or_create(url='http://qliker.ru')
    
    def test_simple(self):
        ''' Проверка правильного перенапраления по qlink '''
        r = self.c.get('/%s' % self.l.code)
        self.assertRedirects(r, 'http://qliker.ru/') # перенаправление на правильную страницу
        
        self.assertEqual(Redirects.objects.filter(link=self.l).count(), 1) # кол-во переходов увеличилось    
        
        
        