from django_logutils.utils import add_items_to_message, log_event, EventLogger


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


def test_log_event(caplog):
    log_event('testevent', **{'type': 'type_1', 'time': 123456})
    assert len(caplog.records()) == 1
    record = caplog.records()[0]
    assert 'event=testevent' in record.msg
    assert 'type=type_1' in record.msg
    assert 'time=123456' in record.msg


def test_event_logger(caplog):
    log_event = EventLogger('my_logger')
    log_event('testevent', **{'type': 'type_1', 'time': 123456})
    assert len(caplog.records()) == 1
    record = caplog.records()[0]
    assert 'event=testevent' in record.msg
    assert 'type=type_1' in record.msg
    assert 'time=123456' in record.msg


def test_event_logger_with_root_logger(caplog):
    log_event = EventLogger()
    log_event('testevent', **{'type': 'type_1', 'time': 123456})
    assert len(caplog.records()) == 1
    record = caplog.records()[0]
    assert 'event=testevent' in record.msg
    assert 'type=type_1' in record.msg
    assert 'time=123456' in record.msg
