from __future__ import absolute_import

import os

from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'authentication',
    'bootstrap3',
    'datetimewidget',
]

# Celery
BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT = 'redis'
CELERYBEAT_SCHEDULE = {
    "send_email": {
        'task': "dashboard.tasks.send_email",
        'schedule': crontab(minute=1, hour=0),
    }
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ajenta_dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

BOOTSTRAP3 = {
    'success_css_class': '',
}

WSGI_APPLICATION = 'ajenta_dashboard.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'users.sqlite3'),
    },
    'ajenta_io': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal2',
        'USER': os.environ['AJENTA_DB_USERNAME'],
        'PASSWORD': os.environ['AJENTA_DB_PASSWORD'],
        'HOST': os.environ['AJENTA_DB_HOST'],
    },
    'platformc': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal2',
        'USER': os.environ['OYDIV_DB_USERNAME'],
        'PASSWORD': os.environ['OYDIV_DB_PASSWORD'],
        'HOST': os.environ['OYDIV_DB_HOST'],
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# E-mail settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# Internationalization
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GB'

USE_I18N = False

USE_L10N = False

USE_TZ = False

DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y/%m/%d')

# Login URL
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

# HTTPS security
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

# Static files
STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATIC_ROOT = os.path.join(STATIC_PATH, 'dashboard_static')

STATICFILES_DIRS = (
    STATIC_PATH,
)
