#-*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Victor Rodionov', 'vito.ordaz@gmail.com'),
)

MANAGERS = ADMINS

import os, sys
PROJECT_DIR = os.path.dirname(__file__)
sys.path.insert(0, PROJECT_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'obrez',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = None

LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'main/static/'),
    os.path.join(PROJECT_DIR, 'ouser/static/'),
)

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = '^^n90(zuujiaz7jd=8!xrbbc$59w3_*$-$wfysbptr)evrqkmr'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'obrez.main.middleware.ProfilerMiddleware',
    'obrez.main.middleware.SetRemoteAddrFromForwardedFor',
)

ROOT_URLCONF = 'qlicker.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'main/templates'),
    os.path.join(PROJECT_DIR, 'ouser/templates'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'obrez.main.context_processors.site',
)

INTERNAL_IPS = (
    '127.0.0.1',
    '192.168.1.5',
)

AUTHENTICATION_BACKENDS = (
    'obrez.ouser.auth_backends.OUserModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    # internal
    'main',
    'ouser',
    'main.templatetags',

    # external
    'sitemetrics',
)

MAX_FOR_DOWNLOAD = 300*1024 # 300Kb

# FAVICONs
FAVICON_ROOT = os.path.join(MEDIA_ROOT, 'favicon')
STANDART_FAVICON = os.path.join(MEDIA_ROOT, 'favicon/standart.png')

#SITE options
SITE_URL = 'http://qliker.ru' if not DEBUG else 'http://127.0.0.1:8000'

# REGISTRATION options
ACTIVATION_DAYS = 14 # 2 недели
DEFAULT_FROM_EMAIL = 'vito.ordaz@gmail.com'

# AUTH options
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/a/login/'

# USERS profiles options
DEFAULT_AVATAR = r"%s%savatars/standart.jpg" % (SITE_URL, STATIC_URL)
DEFAULT_AVATAR_SIZE = 80

# GEOIP_SETTINGS
GEOIP_COUNTRY_FILE = os.path.join(PROJECT_DIR, 'main/geoipdb/GeoIPCountryWhois.csv')
GEOIP_DB_URL = 'http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip'

# OUSER SETTINGS
DEFAULT_AVATAR_WIDTH = 100
DEFAULT_AVATAR_HEIGHT = 100

# QRCode options
QRCODE_DIR = os.path.join(MEDIA_ROOT, 'qrcodes/')
QRCODE_WIDTH = 150

# Services
SERVICES_DIR = os.path.join(MEDIA_ROOT, 'services')

# Twitter application settings
TWITTER_CONSUMER_KEY = 'dDWTQA9y47QwG0AkfhrvUQ'
TWITTER_CONSUMER_SECRET = 'pML25U4f45cF2y1G9KWP2xqdRUwkekFnoZUFY5FChI'
TWITTER_PICTURE_SIZE = 'bigger' # mini(24x24)|normal(48x48)|bigger(73x73)

# Facebook application settings
FB_CLIENT_ID = '194429703930510'
FB_CLIENT_SECRET = 'e4bc0be7df02efe78c926d5935dd28c6'
FB_ACCESS_TOKEN_URI = 'http://127.0.0.1:8000/a/profile/fb/'
FB_PERMISSIONS = 'publish_stream,offline_access'
FB_PICTURE_TYPE = 'normal' # small|normal|large

try:
    from settings_local import *
except ImportError:
    pass
