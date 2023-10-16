import logging
import sys

from vncman.config.color import BOLD_BRIGHT_RED, CYAN, GREY, RED, RESET, YELLOW


class _ColoredLogFormatter(logging.Formatter):
    FMT = "%(name)s: [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: GREY + FMT + RESET,
        logging.INFO: CYAN + FMT + RESET,
        logging.WARNING: YELLOW + FMT + RESET,
        logging.ERROR: RED + FMT + RESET,
        logging.CRITICAL: BOLD_BRIGHT_RED + FMT + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("vncman")
logger.propagate = False
logger.setLevel(logging.INFO)

_stderr_handler = logging.StreamHandler(sys.stderr)
_stderr_handler.setLevel(logging.INFO)
_stderr_handler.setFormatter(_ColoredLogFormatter())

logger.addHandler(_stderr_handler)
