from django.views.generic.base import TemplateView
import os
import traceback
from pathlib import Path

from django.conf import settings
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.contrib import admin


BASE_DIR = Path('__file__').resolve().parent
service_settigs = {
    'BASE_DIR': BASE_DIR,
    'SECRET_KEY': os.getenv('SECRET_KEY', 'django-insecure-$ie'),
    'DEBUG': os.getenv('DEBUG', True),
    'ALLOWED_HOSTS': [],
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'django_filters',
        'service.api.ServiceConfig',
    ],
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    'ROOT_URLCONF': 'service',
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'service'],
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
    ],
    'WSGI_APPLICATION': 'service.application',
    'DATABASES': {
        'default': {
            'ENGINE': os.getenv('DATABASE_ENGINE',
                                'django.db.backends.sqlite3'),
            'NAME': os.getenv('DATABASE_NAME', BASE_DIR / 'db.sqlite3'),
            'HOST': os.getenv('DATABASE_HOST', None),
            'PORT': os.getenv('DATABASE_PORT', None),
        }
    },
    'LANGUAGE_CODE': 'en-us',
    'TIME_ZONE': 'UTC',
    'USE_I18N': True,
    'USE_L10N': True,
    'USE_TZ': True,
    'STATIC_URL': '/static/',
    'DEFAULT_AUTO_FIELD': 'django.db.models.BigAutoField',
    'REST_FRAMEWORK': {
        'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': os.getenv('DRF_PAGE_SIZE', 2),
    },
    'GITHUB_AUTH_TOKEN': os.getenv('GITHUB_AUTH_TOKEN', None)
}

if not settings.configured:
    settings.configure(**service_settigs)

try:
    application = get_wsgi_application()
except Exception:
    traceback.print_exc()


from service.api import repository, user  # noqa: E402
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/github/user/', user.urlpatters),
    path('api/github/repository/', repository.urlpatters),
    url(r'', TemplateView.as_view(template_name='index.html'), name='home'),
]
