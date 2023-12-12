"""
Django settings for delivery_client project.

Программируемые настройки back-and сервера.
"""
from dataclasses import dataclass
from os import mkdir, getenv
from os.path import exists, join
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SITE_ID = 1

# check/create logs folder
if exists(join(BASE_DIR, 'log')):
    pass
else:
    mkdir(join(BASE_DIR, 'log'))


@dataclass(frozen=True)
class Profile:
    """Список профилей настроек проекта"""
    __default = 'default'
    local = 'local'
    development = 'development'
    testing = 'testing'
    production = 'production'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'delivery_client.urls'

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

WSGI_APPLICATION = 'delivery_client.wsgi.application'


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


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# путь к медиа по умолчанию
MEDIA_ROOT = ''
# путь к статике по умолчанию
STATIC_ROOT = ''

INTERNAL_IPS = ['127.0.0.1']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'EXCEPTION_HANDLER': 'apps.authentication.utils.custom_exception_handler'
}

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ENV_NAME = ''

LOG_DIR=Path(BASE_DIR, "log", "logs.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR,
            "formatter": "app",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

# ==================     Import Manager Dynaconf     ========================
# to switch the environment you use:
# $ export SETTINGS_PROFILE=[default | development | production | production_testing]
#   python manage.py
# SETTINGS_PROFILE exported from .env

# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://dynaconf.readthedocs.io/en/latest/guides/django.html
secrets = exists(join(BASE_DIR, 'config', '.secrets.toml'))
env = exists(join(BASE_DIR, 'config', '.env'))
if not secrets or not env:
    raise FileNotFoundError(f'Файл .secrets.toml или .env не обнаружен в '
                            f'папке конфиг. Их необходимо создать на основе'
                            f'\"sample\" файлов.')

import dynaconf  # noqa
from config.config import settings as dyna_settings

# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
# ===========================================================================

switch_settings = getenv('SETTINGS_PROFILE')
if switch_settings not in [Profile.local, Profile.production, Profile.testing,
                           Profile.development]:
    raise SystemExit(f'Внимание не выбрана конфигурация настроек!\n'
                     f'Укажите в .env файле переменной SETTINGS_PROFILE '
                     f'одно из значений - local, develop или production')
print(f'+++ Starting with [{ENV_NAME}] settings. +++')