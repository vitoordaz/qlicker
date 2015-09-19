#-*- coding: utf-8 -*-
'''
Created on 26.03.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''
from django.utils.translation import gettext_lazy as _
from django.test import TestCase

from obrez.main.forms import addLinkForm, addLinkFormAuthenticated

class addLinkFormTest(TestCase):
    def test_empty_data(self):
        ''' Ссылка не введена '''
        # форма не валидна
        form = addLinkForm({'url': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Укажите ссылку'])
        
    def test_not_url(self):
        ''' Не ссылка '''
        # форма не валидна
        form = addLinkForm({'url': 'hello'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Укажите правильную ссылку'])

        form = addLinkForm({'url': 'h://qliker.ru'}) # неправильный протокол
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Укажите правильную ссылку'])
    
    def test_already_qlink(self):
        ''' Уже Qlink '''
        # форма не валидна
        form = addLinkForm({'url': 'qliker.ru/12a'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Уже Qlink'])
        
        form = addLinkForm({'url': 'www.qliker.ru/12a'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Уже Qlink'])
        
        form = addLinkForm({'url': 'http://qliker.ru/12a'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Уже Qlink'])
        
        form = addLinkForm({'url': 'http://www.qliker.ru/12a'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['url'].errors, [u'Уже Qlink'])
    
    def test_url_without_http(self):
        ''' Ссылка без http '''
        # форма валидна
        form = addLinkForm({'url': 'qliker.ru'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form['url'].data, 'qliker.ru')
        
    def test_success(self):
        ''' Нормальная ссылка '''
        # форма валидна
        form = addLinkForm({'url': 'http://qliker.ru'})
        self.assertTrue(form.is_valid())
        
class addLinkFormAuthenticatedTest(TestCase):
    def test_short_not_url(self):
        ''' Сократить -> введена не ссылка '''
        pass