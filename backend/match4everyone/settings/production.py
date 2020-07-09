import logging
import os

from django.utils.log import DEFAULT_LOGGING

from match4everyone.constants.enum import Environment
from match4everyone.settings.common import *  # noqa
from match4everyone.settings.common import IS_FORK, RUN_DIR

logger = logging.getLogger(__name__)

THIS_ENV = Environment.PRODUCTION

DEFAULT_LOGGING["handlers"]["console"]["filters"] = []

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    "matchmedisvsvirus.dynalias.org",
    "helping-health.from-de.com",
    "match4everyone.de",
    "match4everyone.eu",
    "match4everyone.org",
    "medis-vs-covid19.de",
    "localhost",
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB", ""),
        "USER": os.environ.get("POSTGRES_USER", ""),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": "database",
        "PORT": "5432",
    }
}


# =============== MAIL RELAY SERVER CONFIGURATION ===============
# TODO: add environment variable based detection whether we are on prod or staging # noqa: T003
NOREPLY_MAIL = "match4everyone<noreply@match4everyone.de>"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Use API instead of SMTP server
use_sendgrid_api = True

if not IS_FORK:
    if use_sendgrid_api:
        # Using the API
        EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

        # Disable all tracking options
        SENDGRID_TRACK_EMAIL_OPENS = False
        SENDGRID_TRACK_CLICKS_HTML = False
        SENDGRID_TRACK_CLICKS_PLAIN = False

    else:
        # Normal SMTP
        EMAIL_HOST = "smtp.sendgrid.net"
        EMAIL_HOST_USER = "apikey"
        EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(RUN_DIR, "sent_emails")
