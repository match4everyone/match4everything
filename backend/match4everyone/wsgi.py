"""
WSGI config for match4everyone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from gevent import monkey

monkey.patch_all()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "match4everyone.settings.production")

application = get_wsgi_application()
