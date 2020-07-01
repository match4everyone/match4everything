import http.client
import json
import logging
import os

from django.conf import settings
from django.core.checks import Error, register
from django.core.checks import Tags as DjangoTags
from django.core.checks import Warning

from match4everyone.constants.enum import Environment

logger = logging.getLogger(__name__)


def register_check(tag, for_environments, exclude_if_ci=False, exclude_if_fork=False):
    if settings.THIS_ENV in for_environments:
        if not ((settings.IS_FORK and exclude_if_fork) or (settings.IS_CI and exclude_if_ci)):
            return register(tag)
    return lambda x: x


def does_sendgrid_sandbox_mail_work():
    conn = http.client.HTTPSConnection("api.sendgrid.com")

    payload = {
        "personalizations": [
            {
                "to": [{"email": "john.doe@example.com", "name": "John Doe"}],
                "subject": "Hello, World!",
            }
        ],
        "content": [{"type": "text/plain", "value": "Heya!"}],
        "from": {"email": "sam.smith@example.com", "name": "Sam Smith"},
        "reply_to": {"email": "sam.smith@example.com", "name": "Sam Smith"},
        "mail_settings": {"sandbox_mode": {"enable": True}},
    }
    headers = {
        "authorization": "Bearer " + settings.SENDGRID_API_KEY,
        "content-type": "application/json",
    }

    conn.request("POST", "/v3/mail/send", json.dumps(payload), headers)

    res = conn.getresponse()
    # on success, sendgrid returns a 200 OK

    return res.status == 200


class Tags(DjangoTags):
    mail_tag = "mails"
    env_tag = "environment"
    map_tag = "map"


@register_check(Tags.env_tag, [Environment.DEVELOPMENT, Environment.PRODUCTION])
def check_fork(app_configs=None, **kwargs):
    errors = []
    if settings.IS_FORK:
        errors.append(
            Warning(
                "This is a fork of the original 'match4everyone' repo.",
                hint=(
                    "Thanks for forking our repository. Pay attention that Travis CI doesn't test your code "
                    "with sendgrid. If you want to use sendgrid for your tests, "
                    "add your repository name to the list in the if statement for IS_FORK in settings/common.py"
                ),
                id="env.E008",
            )
        )
    return errors


@register_check(Tags.env_tag, [Environment.DEVELOPMENT, Environment.PRODUCTION])
def check_slack_webhook(app_configs=None, **kwargs):
    errors = []
    if os.environ.get("SLACK_LOG_WEBHOOK") is None:
        errors.append(
            Warning(
                "No Slack Webhook for logging set.",
                hint=(
                    "Currently no logging to Slack Channels is configured.\n\t"
                    "This is not necessary, but recommended for production deployment. A key can be generated "
                    "using the documentation at:\n\t"
                    "https://slack.com/intl/en-at/help/articles/115005265063-Incoming-Webhooks-for-Slack\n\t"
                    "To use Slack Error notifications set the webhook in your environment by "
                    "setting the environment variable SLACK_LOG_WEBHOOK to your webhook URL."
                ),
                id="env.E003",
            )
        )
    return errors


@register_check(
    Tags.mail_tag, [Environment.DEVELOPMENT, Environment.PRODUCTION], exclude_if_ci=True
)
def check_map_settings(app_configs=None, **kwargs):
    errors = []

    if settings.LEAFLET_TILESERVER == "open_street_map":
        errors.append(
            Warning(
                "Usage restricted tile server.",
                hint="You are using an open street map tile server for viewing the map, which is subject to usage "
                "restrictions (See https://operations.osmfoundation.org/policies/tiles/)."
                "\nIf you plan to put this system into production, please consider setting up "
                "your own tile server or using a commercial service, e.g. mapbox."
                "We readily provide an integration for mapbox, which you can use by setting LEAFLET_TILESERVER='mapbox'"
                " and adding your API key by setting the environment variable MAPBOX_TOKEN.",
                id="map.W001",
            )
        )
    elif settings.LEAFLET_TILESERVER == "mapbox":
        if settings.MAPBOX_TOKEN is None:
            errors.append(
                Error(
                    "Mapbox token not found.",
                    hint=(
                        "You have to set your Mapbox API token by setting the environment variable MAPBOX_TOKEN."
                    ),
                    id="map.E001",
                )
            )
    elif settings.LEAFLET_TILESERVER == "custom_tile_url":
        if settings.TILE_SERVER_URL is None:
            errors.append(
                Error(
                    "No tile server url found.",
                    hint="You need to provide a url to a tile server with in the following format:\n"
                    "\thttps://c.tile.openstreetmap.org/{z}/{x}/{y}.png' and set this using the environment"
                    " variable TILE_SERVER_URL.",
                    id="map.E002",
                )
            )
    else:
        errors.append(
            Error(
                "Map backend not supported.",
                hint="Please set the LEAFLET_TILESERVER in the environment to 'open_street_map', 'custom_tile_url'"
                " or 'mapbox'.",
                id="map.E002",
            )
        )
    return errors


@register_check(Tags.env_tag, [Environment.DEVELOPMENT, Environment.PRODUCTION])
def check_secret_key(app_configs=None, **kwargs):
    errors = []
    if settings.SECRET_KEY is None:
        errors.append(
            Error(
                "Django secret key not found.",
                hint=(
                    "You have to set the django application secret key in you environment with "
                    "'export SECRET_KEY=<<yourKey>>'."
                ),
                id="env.E002",
            )
        )
    return errors


@register_check(Tags.mail_tag, [Environment.DEVELOPMENT])
def check_sendgrid_dev(app_configs=None, **kwargs):
    errors = []
    if settings.MAIL_RELAY_OPTION == "sendgrid":
        if settings.SENDGRID_API_KEY is None:
            errors.append(
                Error(
                    "Sendgrid API key not found.",
                    hint=(
                        "Your are in development mode, and want to use the sendgrid backend. "
                        "We did not find an API key.\n"
                        "You have to set the Sendgrid API key in you environment by setting the environment variable "
                        "SENDGRID_API_KEY.\n"
                        "If you want to use another backend set 'MAIL_RELAY_OPTION' in the development"
                        " settings to another value, e.g. 'file'."
                    ),
                    id="mails.E003",
                )
            )
        else:
            if not does_sendgrid_sandbox_mail_work():
                errors.append(
                    Error(
                        "You want to use Sendgrid, but sending a mail in sandbox mode fails.",
                        hint=(
                            "Your API key might be invalid, something is up with sendgrid... "
                            "go check it!"
                        ),
                        id="mails.E002",
                    )
                )
    return errors


@register_check(Tags.mail_tag, [Environment.PRODUCTION], exclude_if_fork=True)
def check_sendgrid_prod(app_configs=None, **kwargs):
    errors = []
    if settings.SENDGRID_API_KEY is None:
        errors.append(
            Error(
                "Sendgrid API key not found.",
                hint=(
                    "You have to set the Sendgrid API key in you environment by setting the environment variable "
                    "SENDGRID_API_KEY."
                    "If thats "
                ),
                id="mails.E001",
            )
        )
    else:
        if not does_sendgrid_sandbox_mail_work():
            errors.append(
                Error(
                    "You want to use Sendgrid, but sending a mail in sandbox mode fails.",
                    hint=(
                        "Your API key might be invalid, something is up with sendgrid... "
                        "go check it!"
                    ),
                    id="mails.E002",
                )
            )
    return errors
