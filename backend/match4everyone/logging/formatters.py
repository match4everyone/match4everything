from datetime import datetime
from enum import Enum
import logging

from django.views.debug import SafeExceptionReporterFilter
import json_log_formatter


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warn"
    ERROR = "error"
    CRITICAL = "error"


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """Format an exception so that it prints on a single line."""
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return result  # or format into one line however you want to

    def format(self, record):  # noqa: A003
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            return s.replace("\n", "") + "|"
        return s


class DefaultExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """Format exceptions as is."""
        result = super(DefaultExceptionFormatter, self).formatException(exc_info)
        return result  # or format into one line however you want to

    def format(self, record):  # noqa: A003
        s = super(DefaultExceptionFormatter, self).format(record)
        return s


class DjangoRequestJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):

        extra["level"] = LogLevel[record.levelname].value
        extra["message"] = "[{}]: {}".format(record.name, record.getMessage())
        if "timestamp" not in extra:
            extra["timestamp"] = datetime.utcnow()
        if hasattr(record, "request"):
            request = record.request
            # Overwrite request information in extra, avoid circular references by copying only selected items
            extra["request"] = {}
            if hasattr(request, "user"):
                extra["user"] = request.user.get_username()

            extra["request"]["path"] = getattr(request, "path", "n/a")
            extra["request"]["method"] = getattr(request, "method", "n/a")

            if extra["request"]["method"] == "GET" and hasattr(request, "GET"):
                extra["request"]["get"] = request.GET

            if extra["request"]["method"] == "POST" and hasattr(request, "POST"):
                ser_filter = SafeExceptionReporterFilter()
                extra["request"]["post"] = ser_filter.get_post_parameters(record.request)

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra
