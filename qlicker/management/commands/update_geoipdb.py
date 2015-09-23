import os
import csv
import urllib2
import zipfile

from django.conf import settings
from django.core.management import base

from qlicker.models import country
from qlicker.models import geoipdb


class Command(base.BaseCommand):
    args = ''
    help = 'Update geo ip database'

    def handle(self, *args, **options):
        print 'Downloading file...'
        site = urllib2.urlopen(settings.GEOIP_DB_URL)
        ofile = open('geoipdb.zip', 'wb')
        ofile.write(site.read())
        ofile.close()
        site.close()

        print 'Extracting downloaded zip file...'
        archive = zipfile.ZipFile('geoipdb.zip')
        archive.extractall()
        archive.close()
        os.remove('geoipdb.zip')

        print 'Updating database...'
        with open('GeoIPCountryWhois.csv') as fp:
            for row in csv.reader(fp, delimiter=',', quotechar='"'):
                c, _ = country.Country.objects.get_or_create(code=row[4],
                                                             name=row[5])
                geoipdb.GeoIPdb.objects.get_or_create(country=c, start=row[0],
                                                      end=row[1])
        os.remove('GeoIPCountryWhois.csv')
