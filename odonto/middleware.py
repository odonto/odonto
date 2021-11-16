from django.conf import settings
from django.db import connection
from datetime import datetime
import logging
import time

logger = logging.getLogger('odonto.requestLogger')


def logging_middleware(get_response):
    def middleware(request):
        username = "-"
        extra_log = ""
        start_time = time.time()
        response = get_response(request)
        if hasattr(request, 'user'):
            username = getattr(request.user, 'username', '-')
        req_time = time.time() - start_time
        if settings.DEBUG:
            sql_time = sum(float(q['time']) for q in connection.queries) * 1000
            extra_log += " (%s SQL queries, %s ms)" % (len(connection.queries), sql_time)

        msg = "%s %s %s %s %s (%.02f seconds)%s" % (
            datetime.now(), username, request.method, request.get_full_path(),
            response.status_code, req_time, extra_log
        )
        logger.info(msg)
        return response

    return middleware
