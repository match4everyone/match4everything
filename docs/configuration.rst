Configuration
=================

In order to be suitable for a variety of projects, a lot of configurations can be applied. This page should give you an overview of what is possible and where to change it.


Environment variables
-------------------------
We use environment variables for:

* Configuration (mapview)
* Credentials

This is a complete list of environment variables we use. Their documentation is documented further in their respective topic:

* ``SECRET_KEY``: django-docs_
* ``SENDGRID_API_KEY``: (:ref:`architecture:mail-setup`)
* ``SLACK_LOG_WEBHOOK``: (:ref:`configuration:logging setup`)

* ``LEAFLET_TILESERVER``: (:ref:`architecture:mapview`)
* ``MAPBOX_TOKEN``: (:ref:`architecture:mapview`)
* ``TILE_SERVER_URL``: (:ref:`architecture:mapview`)

* ``POSTGRES_DB``: (:ref:`architecture:production server setup`)
* ``POSTGRES_USER``: (:ref:`architecture:production server setup`)
* ``POSTGRES_PASSWORD``: (:ref:`architecture:production server setup`)

.. _django-docs: https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY

Customize the Participants
-----------------------------

You probably do not want to match hospitals and students, as in the standard setup.
But, you might have something else in mind.
If you know the criteria exactly that you want to acquire from the participants, you can edit their config.

In the django settings file, the app ``match4everyone`` requires you to set

``PARTICIPANT_SETTINGS = {"A": helper_config, "B": institution_config}``

where the latter are both an instance of your customized subclass of ``ParticipantConfig``.
This class allows you to specify the information you would like to gather from each type of participant as well
as the permissions of who can access which type of data.

# Properties

* ``name`` - the name with which this participant group should be referred to on the website itself

* ``properties`` - the list of properties that the participant type should be able to set on signup. The available properties are documented below.


# Permissions

* ``needs_manual_approval_from_staff`` - True by default: determines whether these participants have to be manually approved by the admins. This is a useful feature, if you want to open the platform only to verified accounts or prevent spammers in general, but it can be deactivated by setting it to False.

* ``profile_visible_for_participants_of_different_type`` - True by default: Participants of the other type can view the profile without having matched.


* ``profile_visible_for_participants_of_same_type`` - True by default: Participants of the same type can search and view other participants profiles.


Page contents
-------------------------

* Main Templates
* Reuseable

Logging Setup
-------------------------
