"""
Django settings for baul project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import sweetify
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'app.cliente',
    'app.config',
    'app.facturacion',
    'app.index',
    'app.producto',
    'app.stock',
    'app.usuario',
    'app.cotizacion',
    'app.reporte',
    'sweetify',
    'import_export',  
    'django_crontab',
    'celery',
    'djcelery',
]
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'
IMPORT_EXPORT_USE_TRANSACTIONS = True  
BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

CRONJOBS = [
    # La función temporizada se ejecuta cada 5 minuto
    ('*/5 * * * *', "app.config.cron.notificaciones"),
]

CELERYBEAT_SCHEDULE = {
    'add-every-5-minutes': {
        'task': 'app.config.task.notificaciones',
        'schedule': 'timedelta(seconds=300)'
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'baul.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [  os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'baul.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
          'NAME': os.environ['MYSQL_DATABASE'],
          'USER': os.environ['MYSQL_USER'],
          'PASSWORD': os.environ['MYSQL_PASSWORD'],
          'HOST':  os.environ['MYSQL_HOST'],
          'PORT': os.environ['MYSQL_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
     'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug.log',
        },
        'console': {
             'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout'
        },
        'syslog':{
            'level':'INFO',
            'class': 'logging.handlers.SysLogHandler',
        },
    },
    'loggers':  {
        'oldname':{
            'level': 'WARNING', 'handlers': ['console'],}
        },
    }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT =   os.path.join(BASE_DIR, 'static/')
PDF_ROOT = STATIC_ROOT + "pdf/"
LOGIN_URL = '/perfil/login/'
LOGIN_REDIRECT_URL = '/index/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"