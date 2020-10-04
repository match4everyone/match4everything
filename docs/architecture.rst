Architecture
=================

Quick Anatomy of a Django App
------------------------------

* Links zur Django-Doku
* Backend Management Commands and their use
* System-Checks

Django Administration
------------------------------

Testing
------------------------------
Data Model Configuration
------------------------------

Mapview
------------------------------
Handling statics in Production
------------------------------
Docker Environment
------------------------------
Permission System
------------------------------
Since we extend the default django user management, we also use the built-in django permission system. As described in the `django documentation`_, some permissions are generated automatically by django in a built-in migration. We use a `custom migration`_ in the ``matching``-app to introduce more custom permissions.

Permissions can be checked for with the ``@permission_required('matching.can_send_newsletter')`` `decorator`_ or directly on a user object with ``user.has_perm('matching.can_send_newsletter')`` for example. These methods take into account all permissions the user has, both directly and through groups.

Groups are a great way to organize permissions, you should never assign permissions directly to a user. There is no limit on how many groups a user can be part of. Groups can be thought of as labels/tags and can be used to organize different user groups. Currently, we use the following groups:

* ``is_a``
* ``is_b``
* ``can_view_a``
* ``can_view_b``
* ``approved_a``
* ``approved_b``
* ``perm_user_stats``
* ``perm_access_stats``
* ``perm_approve_a``
* ``perm_approve_b``
* ``perm_send_newsletter``

While some groups are meant for labelling users, such as ``is_a`` or ``approved_a``, most of the groups have permissions attached to them. If you need to change any permission configuration, you can either change our `custom migration`_, or adjust the permissions in the :ref:`architecture:django administration` interface.

.. _django documentation: https://docs.djangoproject.com/en/3.0/topics/auth/default/#permissions-and-authorization
.. _custom migration: https://github.com/match4everyone/match4everything/blob/staging/backend/apps/matching/migrations/0002_permission_group_creation.py
.. _decorator: https://docs.djangoproject.com/en/3.0/topics/auth/default/#the-permission-required-decorator


Securing views
--------------

There are several options available to restrict who can access a view in django. This project mainly uses `class-based views`_. The 'entry point' in class-based views is the ``dispatch``-method, thus this is the method to protect. You can:

* add the method decorator to the dispatch method at class level (``@method_decorator(login_required, name="dispatch")``). This is used a lot in this project to restrict views to logged-in users or staff users. A good example is the `staff profile`_. Note that we use the standard dispatch method from the ``TemplateView`` class, therefore the method does not appear in our code, but the decorator gets added nonetheless.
* add the method decorator directly to the ``dispatch``-method. This is a good option when you already need to override it to add some custom logic. In this case, you can add the ``@login_required`` decorator directly to the method. For consistency reasons, when working with class based views in this repository, decorators are never placed directly on the method, although this would be possible.
* check for permissions after entering the method and raise exceptions when check fails. This is done in the `user info view page`_.
* use `Mixins`_. This project does not use them.

For simple views, `function-based views`_ are sufficient. When using them, you can add decorators directly on the method, like on the `usage statistics view`_.

The discussion on what to use in this project took place in `this pull request`_. It also features more code examples.

.. _class-based views: https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/
.. _user info view page: https://github.com/match4everyone/match4everything/blob/staging/backend/apps/matching/views/participant_info_view.py
.. _staff profile: https://github.com/match4everyone/match4everything/blob/staging/backend/apps/matching/views/staff_profile.py
.. _Mixins: https://docs.djangoproject.com/en/3.0/topics/auth/default/#the-loginrequired-mixin
.. _function-based views: https://docs.djangoproject.com/en/3.0/topics/http/views/
.. _usage statistics view: https://github.com/match4everyone/match4everything/blob/staging/backend/apps/use_statistics/views.py
.. _this pull request: https://github.com/match4everyone/match4everything/pull/43


Mail-Setup
------------------------------
Django-CMS Integration
------------------------------
Javascript&CSS Frontend Components
----------------------------------
Production Server Setup
------------------------------

    Nginx Reverse Proxy

Design Decisions
------------------------------

* Why is Geocoding so extremely hard
* Why Webpack
* Why Django-CMS, or Wagtail, or ...
* Why Sendgrid
