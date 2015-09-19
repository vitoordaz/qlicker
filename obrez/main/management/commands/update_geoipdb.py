#-*- coding: utf-8 -*-

import urllib2, os, csv
from zipfile import ZipFile

from django.core.management.base import BaseCommand
from django.conf import settings

from obrez.main.models import GeoIPdb, Country

class Command(BaseCommand):
    args = ''
    help = 'Update geo ip database'

    def handle(self, *args, **options):
        print "Downloading file..."
        site = urllib2.urlopen(settings.GEOIP_DB_URL)
        ofile = open('geoipdb.zip', 'wb')
        ofile.write(site.read())
        ofile.close()
        site.close()

        print "Extracting downloaded zip file..."
        archive = ZipFile('geoipdb.zip')
        archive.extractall()
        archive.close()
        os.remove('geoipdb.zip')

        print "Updating database..."
        file = open('GeoIPCountryWhois.csv')
        f = csv.reader(file, delimiter=',', quotechar='"')
        for row in f:
            country, created = Country.objects.get_or_create(code=row[4], name=row[5])
            ip_interval = GeoIPdb.objects.get_or_create(country=country, start = row[0], end=row[1])
        file.close()
        os.remove('GeoIPCountryWhois.csv')
