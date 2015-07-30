"""Various utility functions."""
import logging


logger = logging.getLogger(__name__)


def add_items_to_message(msg, log_dict):
    """Utility function to add dictionary items to a log message."""
    out = msg
    for key, value in log_dict.items():
        out += " {}={}".format(key, value)
    return out


def log_event(event, *args, **log_dict):
    """
    Utility function for logging an event (e.g. for metric analysis).
    """
    msg = "event={}".format(event)
    msg = add_items_to_message(msg, log_dict)
    log_dict.update({'event': event})
    logger.info(msg, extra=log_dict)
