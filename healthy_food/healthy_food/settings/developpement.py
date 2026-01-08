from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'purbeurre',
        'USER': 'purbeurre',
        'PASSWORD': '@DB15pm12perso2024@',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
