from django.conf import settings

QUERYTRACER_MODULES = getattr(settings, 'QUERYTRACER_MODULES', (
    'query_tracer.modules.sql.SQLRealTimeModule',
    'query_tracer.modules.sql.SQLSummaryModule',
    'query_tracer.modules.ajax.AjaxDumpModule',
))

QUERYTRACER_FILTER_SQL = getattr(settings, 'QUERYTRACER_FILTER_SQL', False)
QUERYTRACER_TRUNCATE_SQL = getattr(settings, 'QUERYTRACER_TRUNCATE_SQL', True)

QUERYTRACER_TRUNCATE_AGGREGATES = getattr(settings, 'QUERYTRACER_TRUNCATE_AGGREGATES', getattr(settings, 'QUERYTRACER_TRUNCATE_AGGREGATES', False))

# This variable gets set to True when we're running the query_tracer
QUERYTRACER_ACTIVE = False

QUERYTRACER_AJAX_CONTENT_LENGTH = getattr(settings, 'QUERYTRACER_AJAX_CONTENT_LENGTH', 300)
QUERYTRACER_AJAX_PRETTY_PRINT = getattr(settings, 'QUERYTRACER_AJAX_PRETTY_PRINT', False)

# Minimum time a query must execute to be shown, value is in MS
QUERYTRACER_SQL_MIN_DURATION = getattr(settings, 'QUERYTRACER_SQL_MIN_DURATION', None)

QUERYTRACER_AUTO_PROFILE = getattr(settings, 'QUERYTRACER_AUTO_PROFILE', False)
