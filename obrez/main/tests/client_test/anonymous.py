#-*- coding: utf-8 -*-
'''
Created on 09.04.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

from selenium import selenium
import unittest, time, re

class TestLinkAdd(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_link_add(self):
        sel = self.selenium
        #  Подготовка 
        sel.open("http://127.0.0.1:8000")
        sel.delete_cookie("sessionid", "")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        #  Добавляем ссылку 
        sel.type("url", "http://mail.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  Проверяем что ссылка добавилась 
        self.failUnless(sel.is_element_present("link=exact:http://mail.ru/"))
        self.assertEqual(0, sel.get_element_index("css=div.link div.long a[href=http://mail.ru/]"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

class TestPagination(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_pagination(self):
        sel = self.selenium
        sel.open("http://127.0.0.1:8000")
        sel.delete_cookie("sessionid", "")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        # Добавляем 10 ссылок
        sel.type("url", "http://mail.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  1 
        sel.type("url", "http://ya.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  2 
        sel.type("url", "http://rambler.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  3 
        sel.type("url", "http://yandex.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  4 
        sel.type("url", "http://google.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  5 
        sel.type("url", "http://google.com")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  6 
        sel.type("url", "http://myshows.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  7 
        sel.type("url", "http://lenta.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  8 
        sel.type("url", "http://apple.com")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  9 
        sel.type("url", "http://music.yandex.ru")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  10 
        sel.type("url", "http://yandex.com")
        sel.click("code")
        for i in range(60):
            try:
                if not sel.is_visible("loading-status"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        #  11 
        #  Должна появиться пагинация 
        self.failUnless(sel.is_visible("css=#links .paginator"))
        self.assertEqual(2, sel.get_element_index("css=#links .paginator"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
