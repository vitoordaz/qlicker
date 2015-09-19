#-*- coding: utf-8 -*-
'''
Created on 07.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com>
'''

import os, sys

PROJECT_DIR = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0] # doble root directory
print PROJECT_DIR
sys.path.insert(0, PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'obrez.settings'

from django.conf import settings

def download_file(url):
    '''
    Загрузка файла базы данных с сайта settings.GEOIP_DB_URL.
    '''
    print "Downloading file..."
    import urllib2
    site = urllib2.urlopen(url)
    ofile = open('geoipdb.zip', 'wb')
    ofile.write(site.read())
    ofile.close()
    site.close()


def extract():
    '''
    Распаковка скачаного файла.
    '''
    print "Extracting downloaded zip file..."
    from zipfile import ZipFile
    archive = ZipFile('geoipdb.zip')
    archive.extractall()
    archive.close()
    os.remove('geoipdb.zip')

def update_db():
    '''
    Обновление базы данных.
    '''
    print "Saving database..."
    import csv
    from obrez.main.models import GeoIPdb, Country
    file = open('GeoIPCountryWhois.csv')
    f = csv.reader(file, delimiter=',', quotechar='"')
    for row in f:
        country, created = Country.objects.get_or_create(code=row[4], name=row[5])
        ip_interval = GeoIPdb.objects.get_or_create(country=country, start = row[0], end=row[1])
    file.close()
    os.remove('GeoIPCountryWhois.csv')

if __name__ == '__main__':
    download_file(settings.GEOIP_DB_URL)
    extract()
    update_db()