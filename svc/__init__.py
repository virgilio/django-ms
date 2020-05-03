import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '&k6s$-tjiwv42#!)7^+md(-+k=gy)_5d_#n!dd8@=mmc#p%4p('
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'svc.app.Service',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'svc.application'
ROOT_URLCONF = 'src.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'

if not settings.configured:
    sts = {
        k: v for k, v in locals().items()
        if not k.startswith('__') and k.isupper()
    }
    settings.configure(**sts)

application = get_wsgi_application()
