"""Configurações gerais do projeto doubot."""

import os
from os import path
from urllib import parse

import dj_database_url
import dj_email_url
from django.core import exceptions


def get_environment_variable(variable):
    """Obtém o valor de uma variável de ambiente requerida obrigatoriamente pelo projeto."""
    try:
        return os.environ[variable]

    except KeyError:
        raise exceptions.ImproperlyConfigured('You must set {} environment variable.'.format(variable))


def get_path(p):
    """Helper para obter caminhos de arquivos referentes a este módulo de configuração."""
    return path.abspath(path.join(BASE_DIR, p))


def get_name_email(value):
    """Helper para obter nome e email de admins e/ou managers da aplicação."""
    result = []
    for token in value.split(':'):
        name, email = token.split(',')
        result.append((name, email))

    return result


# export ADMINS=username1,email1@domain.com:username2,email2@domain.com
ADMINS = get_name_email(get_environment_variable('ADMINS'))
managers = os.environ.get('MANAGERS', None)
MANAGERS = get_name_email(managers) if managers else ADMINS

# Build paths inside the project like this: join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_environment_variable('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config()
}

# Email
# https://docs.djangoproject.com/en/dev/topics/email/
dj_email_url.SCHEMES.update(postoffice='post_office.EmailBackend')
vars().update(dj_email_url.config())

DEFAULT_CHARSET = os.environ.get('DEFAULT_CHARSET', 'utf-8')  # default charset in django.core.email.
# default from_email in EmailMessage.
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
# default prefix + subject in mail_admins/managers.
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', '[Django]')
# default from: header in mail_admins/managers.
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'admin@localhost')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'diário.apps.DiárioConfig',
    'gunicorn',
    'post_office',
    'storages',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [get_path('../templates')],
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

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

ROOT_URLCONF = 'doubot.urls'

WSGI_APPLICATION = 'doubot.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = get_path('../../static')
STATICFILES_DIRS = (get_path('../static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = get_path('../../media')

LOGIN_REDIRECT_URL = '/'
INTERNAL_IPS = ['127.0.0.1']

redis_url = parse.urlparse(os.environ.get('REDIS_URL'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:{1}'.format(redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'PASSWORD': redis_url.password,
            'DB': 0,
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter',
                                'rest_framework.filters.OrderingFilter')
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
        'TTCC': {
            'class': 'logging.Formatter',
            'format': '%(msecs)d [%(threadName)s] %(levelname)s %(module)s - %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'console_TTCC': {
            'class': 'logging.StreamHandler',
            'formatter': 'TTCC',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'core': {
            'handlers': ['console_TTCC'],
            'level': 'DEBUG',
        },
    }
}
