import json
import logging

from datetime import datetime
from typing import Any
from functools import cache
from pythonjsonlogger import jsonlogger


class TimestampJSONFormatter(jsonlogger.JsonFormatter):

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("@timestamp"):
            now = datetime.isoformat(datetime.now())
            log_record["@timestamp"] = now
        if not log_record.get("message"):
            log_record.pop("message")

    def format(self, record):
        log_record = {
            "message": record.getMessage(),
            "taskName": getattr(record, "taskName", None),
            "@timestamp": getattr(record, "@timestamp", None),
        }
        return json.dumps(log_record, ensure_ascii=False)


@cache
def get_logger() -> logging.Logger:
    logger = logging.getLogger("kibana-logger")
    handler = logging.StreamHandler()
    handler.setFormatter(TimestampJSONFormatter())
    logger.propagate = False
    logger.handlers.clear()
    logger.addHandler(handler)
    return logger
