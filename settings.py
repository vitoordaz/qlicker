# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys


SITE_ID = 1

PROJECT_DIR = os.path.dirname(__file__)
sys.path.insert(0, PROJECT_DIR)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOSTNAME = 'qlicker.co'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6vj0=100e%qi#r3n)v0o-z#d#5^2+8mw-hf&7lk0_*g2&6tdq6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_URL = 'http://qlicker.co' if not DEBUG else 'http://127.0.0.1:8000'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'qlicker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'qlicker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(PROJECT_DIR, 'templates'), ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'qlicker.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'qlicker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

# Qliker user settings
DEFAULT_AVATAR_WIDTH = 100
DEFAULT_AVATAR_HEIGHT = 100


# Facebook application settings
FB_CLIENT_ID = '194429703930510'
FB_CLIENT_SECRET = 'e4bc0be7df02efe78c926d5935dd28c6'
FB_ACCESS_TOKEN_URI = 'http://127.0.0.1:8000/a/profile/fb/'
FB_PERMISSIONS = 'publish_stream,offline_access'
FB_PICTURE_TYPE = 'normal'  # small|normal|large

# REGISTRATION options
ACTIVATION_DAYS = 14  # 2 weeks
DEFAULT_FROM_EMAIL = 'noreply@qlicker.co'

# AUTH options
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/a/login/'

# GEOIP_SETTINGS
GEOIP_COUNTRY_FILE = os.path.join(PROJECT_DIR, 'tmp', 'GeoIPCountryWhois.csv')
GEOIP_DB_URL = ('http://geolite.maxmind.com/download/geoip/database/'
                'GeoIPCountryCSV.zip')

# S3
QR_CODES_BUCKET = 'qlicker-qr-codes'

MAX_FOR_DOWNLOAD = 300 * 1024  # 300Kb

try:
    from local_settings import *
except ImportError:
    pass