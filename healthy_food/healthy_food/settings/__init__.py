from .base import *

env_type = os.environ.get('ENV_TYPE', 'local')

if env_type == 'production':
    from .production import *
else:
    from .developpement import *