from .base import *
import dj_database_url


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Use the Render DB
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# WhiteNoise optimization for production (static file compression)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production-specific security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True