"""
ASGI config for match4everyone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from gevent import monkey

monkey.patch_all()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "match4everyone.settings.production")

application = get_asgi_application()
