from .base import *


DEBUG = os.environ.get('DEBUG') == 'True'
if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['pur-beurre.onrender.com']

db_from_env = dj_database_url.config(conn_max_age=600)

# Use the Render DB
if db_from_env:
    DATABASES['default'] = db_from_env
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL','sqlite:///db.sqlite3'),
#         conn_max_age=600
#     )
# }
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# WhiteNoise optimization for production (static file compression)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Production-specific security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'error.log',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'ERROR',
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
