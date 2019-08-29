import os
import django
from channels.routing import get_default_application


env = os.environ.get('PROJECT_ENV', 'dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_xops.settings.{}'.format(env))
django.setup()
application = get_default_application()
