#-*- coding: utf-8 -*-
'''
Created on 09.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from selenium import selenium
import unittest, time, re

class TestAuthenticatedPagination(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_pagination(self):
        ''' 
        Тест проверяющий появление пагинации на главное странице 
        авторизованных пользователей при добавление большого количества ссылок
        '''
        sel = self.selenium
        # Подготовка
        sel.delete_cookie("sessionid", "")
        # Логинимся
        sel.open("http://127.0.0.1:8000/a/login/")
        sel.type("username", "admin")
        sel.type("password", "password")
        sel.click(u"css=input[value=\"Войти\"]")
        sel.wait_for_page_to_load("30000")
        # Добавляем ссылки
        # 10
        sel.type("url", "http://yandex.ru, http://rambler.ru, http://yandex.com, http://mail.ru, http://mail.com, http://bit.ly, http://google.ru, http://google.com, http://ya.ru, http://python.org")
        sel.click("short")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # ещё одна
        sel.type("url", "http://apple.com")
        sel.click("short")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # Проверяем пагинацию
        self.failUnless(sel.is_visible("css=#links .paginator"))
        self.assertEqual(2, sel.get_element_index("css=#links .paginator"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

class TestAuthenticatedPaginationArchivate(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_paginator_archivate(self):
        ''' Тест: скрытие пагинации при помещения в архив большого количества ссылок '''
        sel = self.selenium
        # Подготовка
        sel.delete_cookie("sessionid", "")
        # Логинимся
        sel.open("http://127.0.0.1:8000/a/login/")
        sel.type("username", "admin")
        sel.type("password", "password")
        sel.click(u"css=input[value=\"Войти\"]")
        sel.wait_for_page_to_load("30000")
        # Добавляем ссылки
        # 10
        sel.type("url", "http://yandex.ru, http://rambler.ru, http://yandex.com, http://mail.ru, http://mail.com, http://bit.ly, http://google.ru, http://google.com, http://ya.ru, http://python.org")
        sel.click("short")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # ещё одна
        sel.type("url", "http://sex.com")
        sel.click("short")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # Проверяем пагинацию
        self.failUnless(sel.is_visible("css=#links .paginator"))
        self.assertEqual(2, sel.get_element_index("css=#links .paginator"))
        # Отправляем в архив
        # 1
        sel.click("//div[@id='links-list']/div[1]/div[6]/span")
        sel.click(u"link=В архив")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # 2
        sel.click("//div[@id='links-list']/div[1]/div[6]/span")
        sel.click(u"link=В архив")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # 3
        sel.click("//div[@id='links-list']/div[1]/div[6]/span")
        sel.click(u"link=В архив")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if not sel.is_visible("css=#links .paginator"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # Пагинация должна исчезнуть
        self.failIf(sel.is_visible("css=#links .paginator"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

class TestAuthenticatedInlineTitleEdit(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_inline_title_edit(self):
        ''' Тест: редактирование заголовка ссылки '''
        sel = self.selenium
        # Подготовка
        sel.delete_cookie("sessionid", "")
        # Логинимся
        sel.open("http://127.0.0.1:8000/a/login/")
        sel.type("username", "admin")
        sel.type("password", "password")
        sel.click(u"css=input[value=\"Войти\"]")
        sel.wait_for_page_to_load("30000")
        # Добавляем ссылку
        sel.type("url", "http://yandex.ru")
        sel.click("short")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # Изменяем title
        sel.click("//div[@id='links-list']/div[1]/div[6]/span")
        sel.click(u"link=Изменить")
        sel.type("title", "Rambler 1")
        sel.click(u"//input[@value='Сохранить']")
        try: self.failUnless(sel.is_text_present("Rambler 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        # Обновляем страницу
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        # Проверяем
        try: self.failUnless(sel.is_text_present("Rambler 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        # Снова меняем
        sel.click("//div[@id='links-list']/div[1]/div[6]/span")
        sel.click(u"link=Изменить")
        sel.type("title", "Rambler 1")
        sel.click(u"//input[@value='Сохранить']")
        try: self.failUnless(sel.is_text_present("Rambler 1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()