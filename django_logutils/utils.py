"""Various utility functions."""


def add_items_to_message(msg, log_dict):
    """Utility function to add dictionary items to a log message."""
    out = msg
    for key, value in log_dict.items():
        out += " {}={}".format(key, value)
    return out
