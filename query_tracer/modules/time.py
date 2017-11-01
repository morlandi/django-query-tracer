import datetime

from query_tracer.modules import QueryTracerModule
from ..utils.time import ms_from_timedelta


class TimeModule(QueryTracerModule):
    """
    Dumps the content of all AJAX responses.
    """

    logger_name = 'time'
    start = None
    stop = None

    def process_init(self, request):
        self.start = datetime.datetime.now()

    def process_complete(self, request):
        self.stop = datetime.datetime.now()
        duration = ms_from_timedelta(self.stop - self.start)
        self.logger.info('duration: %.3f ms' % duration)
