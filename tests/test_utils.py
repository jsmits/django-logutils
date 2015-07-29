from django_logutils.utils import add_items_to_message


def test_add_items_to_message():
    msg = "log message"
    items = {'user': 'benny', 'email': 'benny@example.com'}
    msg = add_items_to_message(msg, items)
    assert msg == 'log message user=benny email=benny@example.com'
