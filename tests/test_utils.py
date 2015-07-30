from django_logutils.utils import add_items_to_message


def test_add_items_to_message():
    msg = "log message"
    items = {'user': 'benny', 'email': 'benny@example.com'}
    msg = add_items_to_message(msg, items)
    assert msg.startswith('log message')
    assert 'user=benny' in msg
    assert 'email=benny@example.com' in msg


def test_add_items_to_message_with_empty_items():
    msg = "log message"
    items = {}
    msg = add_items_to_message(msg, items)
    assert msg == 'log message'
