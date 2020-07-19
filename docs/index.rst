.. match4everything documentation master file, created by
   sphinx-quickstart on Thu Jul  9 18:42:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to match4everything's documentation!
============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   first_steps
   development
   deployment



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


How can I write this documentation?
===================================
Have a look at the `primer`_ and the `quick rst guide`_.
You can build it with cd docs && docker-compose up -d --build && docker-compose run documentation make html
and find the html files in docs/_build.

.. _`quick rst guide`: https://docutils.sourceforge.io/docs/user/rst/quickref.html
.. _primer: https://docutils.sourceforge.io/docs/user/rst/quickstart.html
