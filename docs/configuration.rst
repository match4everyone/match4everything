Configuration
=================

In order to be suitable for a variety of projects, a lot of configurations can be applied. This page should give you an overview of what is possible and where to change it.


Environment variables
-------------------------
We use environment variables for:

* Configuration

  * choosing a mapview backend that delivers the map tiles (square pngs of the map at a certain zoom level) to the user. For more technical information, refer to :ref:`architecture:mapview`.

* Credentials

  * sendgrid key (if you use sendgrid as the mail service) (See :ref:`architecture:mail-setup`)
  * mapbox token (if you use mapbox as a tile server) (See :ref:`architecture:mapview`)

This is a complete list of environment variables we use. Their documentation is documented further in their respective topic:

* ``SECRET_KEY``: django-docs_
* ``SENDGRID_API_KEY``: (:ref:`mail-setup`)
* ``SLACK_LOG_WEBHOOK``: (:ref:`logging setup`)


* ``LEAFLET_TILESERVER``: (:ref:`architecture:mapview`)
* ``MAPBOX_TOKEN``: (:ref:`architecture:mapview`)
* ``TILE_SERVER_URL``: (:ref:`architecture:mapview`)

* ``POSTGRES_DB``: (:ref:`architecture:production server setup`)
* ``POSTGRES_USER``: (:ref:`architecture:production server setup`)
* ``POSTGRES_PASSWORD``: (:ref:`architecture:production server setup`)

.. _django-docs: https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY


Model Setup
-------------------------

Page contents
-------------------------

* Main Templates
* Reuseable

Logging Setup
-------------------------
