import json

from query_tracer.modules import QueryTracerModule
from query_tracer import settings


class AjaxDumpModule(QueryTracerModule):
    """
    Dumps the content of all AJAX responses.
    """

    logger_name = 'ajax'

    def process_response(self, request, response):
        if request.is_ajax():
            # Let's do a quick test to see what kind of response we have
            if len(response.content) < settings.QUERYTRACER_AJAX_CONTENT_LENGTH:
                content = response.content
                if settings.QUERYTRACER_AJAX_PRETTY_PRINT:
                    content = json.dumps(json.loads(content), indent=4)
                self.logger.info(content)
