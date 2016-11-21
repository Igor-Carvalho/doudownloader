"""Configurações de pré-produção."""

from .base import *

# Security
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
ALLOWED_HOSTS = ['*']

# cache
MIDDLEWARE = (['django.middleware.cache.UpdateCacheMiddleware'] +
              MIDDLEWARE +
              ['django.middleware.cache.FetchFromCacheMiddleware'])

# amazon s3
# AWS_STORAGE_BUCKET_NAME = 'tecnocracias-staging'
# AWS_ACCESS_KEY_ID = get_environment_variable('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = get_environment_variable('AWS_SECRET_ACCESS_KEY')
# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'core.storages.StaticLocationStorage'
# MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'core.storages.MediaLocationStorage'
