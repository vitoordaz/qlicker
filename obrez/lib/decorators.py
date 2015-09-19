#-*- coding: utf-8 -*-
'''
Created on 13.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

class execution_time(object):
    '''
    Декоратор для определения время выполнения функции
    '''
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kargs):
        from datetime import datetime
        t1 = datetime.now()
        result = self.func(*args, **kargs)
        t2 = datetime.now()
        delta = t2 - t1
        print "Function %s execution time is %s mcs" % (self.func.__name__, delta.microseconds)
        return result
    def __repr__(self):
        return self.func.__doc__