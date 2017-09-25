=============================
django-query-tracer
=============================

.. image:: https://badge.fury.io/py/django-query-tracer.svg
    :target: https://badge.fury.io/py/django-query-tracer

.. image:: https://travis-ci.org/morlandi/django-query-tracer.svg?branch=master
    :target: https://travis-ci.org/morlandi/django-query-tracer

.. image:: https://codecov.io/gh/morlandi/django-query-tracer/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/morlandi/django-query-tracer

A simplified version of django-devserver limited to SQL tracing and Ajax dump.

Motivations
-----------

django-devserver is a very nice and usefull package, but the project isn't very active,
and occasional problems related to new Django versions stay unfixed for long time even
when a solution is available as PR.

Being mostly interested in tracing db queries, I finally decided to package a
stripped down version of the project.

Quickstart
----------

Install django-query-tracer::

    pip install django-query-tracer

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'query_tracer',
        ...
    )

Add django-query-tracer's middleware:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        ...
        'query_tracer.middleware.QueryTracerMiddleware',
        ...
    ]

Features
--------

See file "query_tracer/settings.py" for available options, and refer to
`django-devserver doc <https://github.com/dcramer/django-devserver>`_ for usage/

Credits
-------

This project is a stripped down version of:

*  django-devserver

.. _django-devserver: https://github.com/dcramer/django-devserver


Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
