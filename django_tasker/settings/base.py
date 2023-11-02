from pathlib import Path
from decouple import config, Csv
import os
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

CORS_ORIGIN_WHITELIST= config('CORS_ORIGIN_WHITELIST', default=[], cast=Csv())

# Para permitir el envío de cookies/tokens de autenticación
CORS_ALLOW_CREDENTIALS = True

ENV_ROLE = config('ENV_ROLE', default='local')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    # Apps del proyecto
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps de terceros
    'drf_yasg',
    'rest_framework',
    'django_filters',
    'django_rest_passwordreset',
    
    # Apps locales
    'apps.core',
    'apps.home',
    'apps.tasks',
    'apps.users',
]

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default=[])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'django_tasker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'django_tasker.wsgi.application'


# RUNNING_UNIT_TESTS = 'test' in os.sys.argv
RUNNING_COLLECTSTATIC = 'collectstatic' in os.sys.argv

# Aseguramos con Argon2PasswordHasher que las contraseñas se guarden en argon2
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher", # Se coloca Argon2 primero para que guarde las claves en argon2 pero que valide con todos los hashers y actualice según se necesite.
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)

APP_LOGLEVEL = config('APP_LOGLEVEL', default='INFO')

# Media Config
MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
    ],
}

# Fecha de expiración del token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

# AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def get_db_config():
    if ENV_ROLE == 'local':
        return {
            'NAME': config('LOCAL_DB_NAME'),
            'USER': config('LOCAL_DB_USER'),
            'PASSWORD': config('LOCAL_DB_PASSWORD'),
            'HOST': config('LOCAL_DB_HOST'),
            'PORT': config('LOCAL_DB_PORT'),
        }
    elif ENV_ROLE == 'develop':
        return {
            'NAME': config('DEV_DB_NAME'),
            'USER': config('DEV_DB_USER'),
            'PASSWORD': config('DEV_DB_PASSWORD'),
            'HOST': config('DEV_DB_HOST'),
            'PORT': config('DEV_DB_PORT'),
        }
    elif ENV_ROLE == 'qa':
        return {
            'NAME': config('QA_DB_NAME'),
            'USER': config('QA_DB_USER'),
            'PASSWORD': config('QA_DB_PASSWORD'),
            'HOST': config('QA_DB_HOST'),
            'PORT': config('QA_DB_PORT'),
        }
    elif ENV_ROLE == 'production':
        return {
            'NAME': config('PROD_DB_NAME'),
            'USER': config('PROD_DB_USER'),
            'PASSWORD': config('PROD_DB_PASSWORD'),
            'HOST': config('PROD_DB_HOST'),
            'PORT': config('PROD_DB_PORT'),
        }
    else:
        raise ValueError("Valor inválido para ENV_ROLE en .env")