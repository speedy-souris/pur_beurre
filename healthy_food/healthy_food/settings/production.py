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

# WhiteNoise optimization for production (static file compression)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production-specific security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True