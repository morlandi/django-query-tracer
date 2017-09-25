=====
Usage
=====

To use django-query-tracer in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'query_tracer.apps.QueryTracerConfig',
        ...
    )

Add django-query-tracer's URL patterns:

.. code-block:: python

    from query_tracer import urls as query_tracer_urls


    urlpatterns = [
        ...
        url(r'^', include(query_tracer_urls)),
        ...
    ]
