import logging
from dotenv import dotenv_values

to_log_or_not_to_log = logging.INFO if dotenv_values(
    "settings.env")["PRINT_ALL_PROGRESS"] == "true" else logging.CRITICAL


PROGRESS_LOG = logging.getLogger("PROGRESS")
PROGRESS_LOG.setLevel(to_log_or_not_to_log)

_ch = logging.StreamHandler()
_ch.setLevel(to_log_or_not_to_log)

_formatter = logging.Formatter(
    fmt='[ %(relativeCreated)08d ] :: %(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S'
)

_ch.setFormatter(_formatter)
PROGRESS_LOG.addHandler(_ch)
