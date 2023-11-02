from .base import *
import os
import mimetypes
from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=DEBUG)

CORS_ALLOW_HEADERS = [
    'accept',
    'accepts',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        **get_db_config(),
    }
}

# Swagger Settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,  # Desactiva la autenticación por sesión
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}