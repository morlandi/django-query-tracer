"""
Based on initial work from django-debug-toolbar
"""
import re

from datetime import datetime

try:
    from django.db import connections
except ImportError:
    # Django version < 1.2
    from django.db import connection
    connections = {'default': connection}

try:
    from django.db.backends import utils # renamed in django 1.7
except ImportError:
    from django.db.backends import util as utils # removed in django 1.9
from django.conf import settings as django_settings
#from django.template import Node

from query_tracer.modules import QueryTracerModule
#from query_tracer.utils.stack import tidy_stacktrace, get_template_info
from query_tracer.utils.time import ms_from_timedelta
from query_tracer import settings

try:
    import sqlparse
except ImportError:
    class sqlparse:
        @staticmethod
        def format(text, *args, **kwargs):
            return text


_sql_fields_re = re.compile(r'SELECT .*? FROM')
_sql_aggregates_re = re.compile(r'SELECT .*?(COUNT|SUM|AVERAGE|MIN|MAX).*? FROM')


def truncate_sql(sql, aggregates=True):
    if not aggregates and _sql_aggregates_re.match(sql):
        return sql
    return _sql_fields_re.sub('SELECT ... FROM', sql)

# # TODO:This should be set in the toolbar loader as a default and panels should
# # get a copy of the toolbar object with access to its config dictionary
# SQL_WARNING_THRESHOLD = getattr(settings, 'QUERYTRACER_CONFIG', {}) \
#                             .get('SQL_WARNING_THRESHOLD', 500)

try:
    from debug_toolbar.panels.sql import DatabaseStatTracker
    debug_toolbar = True
except ImportError:
    debug_toolbar = False
    import django
    #version = float('.'.join([str(x) for x in django.VERSION[:2]]))
    #if version >= 1.6:

    # Version comparison fix required after Django 1.10
    version = django.VERSION[0] * 100 + django.VERSION[1]
    if version >= 106:
        DatabaseStatTracker = utils.CursorWrapper
    else:
        DatabaseStatTracker = utils.CursorDebugWrapper

class DatabaseStatTracker(DatabaseStatTracker):
    """
    Replacement for CursorDebugWrapper which outputs information as it happens.
    """
    logger = None
    queries = []


    def execute(self, sql, params=()):
        if params is None:
            formatted_sql = sql
        elif isinstance(params, dict):
            formatted_sql = sql % params
        else:
            formatted_sql = sql % tuple(params)
            
        if self.logger:
            message = formatted_sql
            if settings.QUERYTRACER_FILTER_OUT_SQL:
                if any(filter_.search(message) for filter_ in settings.QUERYTRACER_FILTER_OUT_SQL):
                    message = None
            if settings.QUERYTRACER_FILTER_IN_SQL:
                if not all(filter_.search(message) for filter_ in settings.QUERYTRACER_FILTER_IN_SQL):
                    message = None
            if message is not None:
                if settings.QUERYTRACER_TRUNCATE_SQL:
                    message = truncate_sql(message, aggregates=settings.QUERYTRACER_TRUNCATE_AGGREGATES)
                message = sqlparse.format(message, reindent=True, keyword_case='upper')
                self.logger.debug(message)

        start = datetime.now()

        try:
            return super(DatabaseStatTracker, self).execute(sql, params)
        finally:
            stop = datetime.now()
            duration = ms_from_timedelta(stop - start)

            if self.logger and (not settings.QUERYTRACER_SQL_MIN_DURATION
                    or duration > settings.QUERYTRACER_SQL_MIN_DURATION):
                if self.cursor.rowcount >= 0 and message is not None:
                    self.logger.debug('Found %s matching rows', self.cursor.rowcount, duration=duration)

            if not (debug_toolbar or django_settings.DEBUG):
                self.db.queries.append({
                    'sql': formatted_sql,
                    'time': duration,
                })
            else:
                self.queries.append({
                    'sql': formatted_sql,
                    'time': duration,
                })

    def executemany(self, sql, param_list):
        start = datetime.now()
        try:
            return super(DatabaseStatTracker, self).executemany(sql, param_list)
        finally:
            stop = datetime.now()
            duration = ms_from_timedelta(stop - start)

            if self.logger:
                message = sqlparse.format(sql, reindent=True, keyword_case='upper')

                message = 'Executed %s times\n' % message

                self.logger.debug(message, duration=duration)
                self.logger.debug('Found %s matching rows', self.cursor.rowcount, duration=duration, id='query')

            if not (debug_toolbar or settings.DEBUG):
                self.db.queries.append({
                    'sql': '%s times: %s' % (len(param_list), sql),
                    'time': duration,
                })
            else:
                self.queries.append({
                    'sql': '%s times: %s' % (len(param_list), sql),
                    'time': duration,
                })


class SQLRealTimeModule(QueryTracerModule):
    """
    Outputs SQL queries as they happen.
    """

    logger_name = 'sql'

    def process_init(self, request):

        if not issubclass(utils.CursorDebugWrapper, DatabaseStatTracker):
            self.old_cursor = utils.CursorDebugWrapper
            utils.CursorDebugWrapper = DatabaseStatTracker
            utils.CursorDebugWrapper.queries = []

        DatabaseStatTracker.logger = self.logger

    def process_complete(self, request):

        if issubclass(utils.CursorDebugWrapper, DatabaseStatTracker):

            # Mimic SQLSummaryModule
            queries = utils.CursorDebugWrapper.queries
            num_queries = len(queries)
            if num_queries:
                unique = set([s['sql'] for s in queries])
                prompt = 'SQL Summary %s ' % ('.' * 58)
                self.logger.info(prompt + '[%(calls)s queries with %(dupes)s duplicates]' % dict(
                    calls=num_queries,
                    dupes=num_queries - len(unique),
                #), duration=sum(float(c.get('time', 0)) for c in queries) * 1000)
                ))

            utils.CursorDebugWrapper = self.old_cursor


class SQLSummaryModule(QueryTracerModule):
    """
    Outputs a summary SQL queries.
    """

    logger_name = 'sql'

    def process_complete(self, request):
        queries = [
            q for alias in connections
            for q in connections[alias].queries
        ]
        num_queries = len(queries)
        if num_queries:
            unique = set([s['sql'] for s in queries])
            self.logger.info('%(calls)s queries with %(dupes)s duplicates' % dict(
                calls=num_queries,
                dupes=num_queries - len(unique),
            ), duration=sum(float(c.get('time', 0)) for c in queries) * 1000)
