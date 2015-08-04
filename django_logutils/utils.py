"""Various utility functions."""
import logging


root_logger = logging.getLogger()


def add_items_to_message(msg, log_dict):
    """Utility function to add dictionary items to a log message."""
    out = msg
    for key, value in log_dict.items():
        out += " {}={}".format(key, value)
    return out


def log_event(event, logger=root_logger, **log_dict):
    """
    Utility function for logging an event (e.g. for metric analysis).

    If no logger is given, fallback to the root logger.

    """
    msg = "event={}".format(event)
    msg = add_items_to_message(msg, log_dict)
    log_dict.update({'event': event})
    logger.info(msg, extra=log_dict)


class EventLogger(object):
    """
    EventLogger class that wrap the log_event function by optionally using an
    existing logger.

    Usage:
    >>> log_event = EventLogger('my_logger')
    >>> log_event('my_event', {'action': 'push_button'})

    """
    def __init__(self, logger_name=None, *args, **kwargs):
        """Initialize the EventLogger

        :param logger_name: name of the logger, e.g. 'my_logger' or __name__
        """
        if logger_name:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = root_logger

    def __call__(self, event, *args, **log_dict):
        """Call the log_event function."""
        log_event(event, logger=self.logger, **log_dict)
