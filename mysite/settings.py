"""
Django settings for exquisitecorpse project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import socket


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', False)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Required by `allauth` template tags
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                # allauth specific context processors
                'allauth.account.context_processors.account',
                'allauth.socialaccount.context_processors.socialaccount',

            ],
        },
    },
]

# all auth doesn't look in templates above apparently
TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by `allauth` template tags
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    # `allauth` specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'crispy_forms',
    'rest_framework',
    # Authentication
    'rest_framework.authtoken',
    'rest_auth',
    # Registration
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    # Social authentication
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    'corsheaders',
    'api',
    'exquisitecorpse'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if socket.gethostname() == 'Joels-MacBook-Pro.local':
    # Local database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'exquisite_corpse',
            'USER': 'jschnall',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
else:
    # Heroku database
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

# Django sites
SITE_ID = 1

# allauth
LOGIN_REDIRECT_URL = '/'

# crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'PAGINATE_BY': 10,                 # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
}

CORS_ORIGIN_WHITELIST = (
)

EXQUISITE_CORPSE = {
    'PAGINATE_BY': 10,
    'NAV_PAGINATE_BY': 5,
}

