# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from query_tracer.urls import urlpatterns as query_tracer_urls

urlpatterns = [
    url(r'^', include(query_tracer_urls, namespace='query_tracer')),
]
