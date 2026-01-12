from .base import *


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
# SECURITY WARNING: keep the secret key used in production secret!

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
