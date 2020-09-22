First Steps
=============

After setting up our system according to :doc:`getting_started` you probably wonder how to make it to your matching site.
We have several ways to change the look and behavior of the site:

1. As you already done following the :doc:`getting_started` guide,
   you can change the configuration for matching partner A and B in
   backend/match4everyone/configuration/A.py and backend/match4everyone/configuration/B.py.

2. You can change the texts on the different sites using django-cms_ which is accessible at django-admin_.
   The section `How to Use Django-CMS`_ will describe the usage further.

3. You can easily change the whole appearance of the website if you change the theme-colors in `frontend/src/css/bootstrap-customization.scss`_

4. You can change all the functionality implemented in Python and the django templates
   in backend/templates/ and backend/apps/matching/templates/.

.. _frontend/src/css/bootstrap-customization.scss: https://github.com/match4everyone/match4everything/blob/staging/frontend/src/css/bootstrap-customization.scss

How to Use Django-CMS
-------------------------

.. _django-cms: https://github.com/divio/django-cms
.. _django-admin: http://localhost:8000/django-administration/
