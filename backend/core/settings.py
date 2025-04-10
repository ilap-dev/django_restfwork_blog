"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import environ
from pathlib import Path

from django.conf.global_settings import DEFAULT_FILE_STORAGE, \
    STATICFILES_STORAGE
from tutorial.settings import INSTALLED_APPS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

VALID_API_KEYS = env.str("VALID_API_KEYS").split(",")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'apps.blog',
    'apps.media',
]

THIRD_PARTY_APPS=[
    'rest_framework',
    'channels',
    'ckeditor',
    'ckeditor_uploader',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework_api',
    'storages',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':'full',
         'autoParagraph':False
    }
}

CKEDITOR_UPLOAD_PATH = 'media/'

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

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':'full',
         'autoParagraph':False
    }
}

CKEDITOR_UPLOAD_PATH = 'media/'

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': 5432,
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
#STATIC_LOCATION = 'static'
#STATIC_URL = 'static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#MEDIA_URL = 'media/'
#MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    #Si una persona esta autenticada puede hacer uso completo del CRUD
    #Sino solo puede hacer uso de los get
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.AllowAny"
    ]
}

REDIS_HOST = env("REDIS_HOST")

#se usa uvicorn y channels para usar asgi, y nuestra aplicacion sea mas rapida
CHANNELS_LAYERS = {
    "default":{
        "BACKEND":"channels_redis.core.RedisChannelLayer",
        "CONFIG":{
            "hosts":[env("REDIS_URL")]
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    }
}

CHANNELS_ALLOWED_ORIGINS = "http://localhost:3000"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Mexico_City"

CELERY_BROKER_URL = env("REDIS_URL")
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600,
    'socket_timeout': 5,
    'retry_on_timeout': True
}

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_IMPORTS = (
    'core.tasks',
    'apps.blog.tasks'
)
# para migrar las base de datos de celery beat, usar en una line de comandos bash:
# python manage.py migrate django_celery_beat
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {}

#Configuraciones de Cloudfront
AWS_CLOUDFRONT_DOMAIN=env("AWS_CLOUDFRONT_DOMAIN")
AWS_CLOUDFRONT_KEY_ID=env.str("AWS_CLOUDFRONT_KEY_ID").strip()
AWS_CLOUDFRONT_KEY=env.str("AWS_CLOUDFRONT_KEY", multiline=True).encode('ascii').strip()

#Configuraciones de AWS
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN
AWS_S3_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
#AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

#Configuracion de seguridad y permisos
AWS_QUERYSTRING_AUTH = False #Deshabilita las firmas en las URLS (archivos publicos)
AWS_FILE_OVERWRITE = False #Deshabilita sobreescribir archivos con el mismo nombre
AWS_DEFAULT_ACL = None #Define el control de accesp predeterminado como publico
AWS_QUERYSTRING_EXPIRE = 5 #Tiempo de expiracion de las URLS firmadas

#Parametros adicionales para los objetos de S3
AWS_S3_OBJECT_PARAMETERS ={
    "CacheControl":"max-age=86400" #Habilita el almacenamiento en cache por un día
}

#Configuracion de Archivos Estaticos
STATIC_LOCATION = "static"
STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
STATICFILES_STORAGE = 'core.storage_backends.StaticStorage'
#STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_LOCATION = "media"
MEDIA_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
#MEDIA_ROOT = MEDIA_URL

#Configuracion de almacenamiento predeterminado
DEFAULT_FILE_STORAGE = "core.storage_backends.PublicMediaStorage"



