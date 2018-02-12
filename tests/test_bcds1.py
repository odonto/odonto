from fp17.bcds1 import BCDS1Message


def test_simple():
    msg = BCDS1Message()
    assert 'clrn' in msg.errors

    msg.set_value('clrn', '')
    assert 'clrn' in msg.errors

    msg.set_value('clrn', '12345')
    assert 'clrn' in msg.errors

    msg.set_value('clrn', '1234567')
    assert 'clrn' in msg.errors

    msg.set_value('clrn', '123456')
    assert not msg.errors

    root = msg.generate_xml()
    BCDS1Message.validate_xml(root)
