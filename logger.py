import logging
import datetime
import time
from dotenv import dotenv_values


class Log:
    def __init__(self):
        self._enabled = logging.INFO if dotenv_values(
            "settings.env")["PRINT_ALL_PROGRESS"] == "true" else logging.CRITICAL

        self._start = datetime.datetime.now()

    def _ms_elapsed(self) -> int:
        """Return roughly the number of milliseconds elapsed between the start of the log and the time this method is called."""
        return int((datetime.datetime.now() - self._start).total_seconds() * 1000)

    def log(self, message: str):
        """Log a message with specific formatting"""
        print(f"[ {self._ms_elapsed():0>10} ] ::  LOG  :: {message}")


PROGRESS_LOG = Log()
