from fp17.bcds1 import BCDS1Message


def test_simple():
    msg = BCDS1Message()

    errors = msg.get_errors()
    assert 'required field' in errors['clrn']

    msg.clrn = '12345'
    errors = msg.get_errors()
    assert 'min length is 6' in errors['clrn']

    msg.clrn = '1234567'
    errors = msg.get_errors()
    assert 'max length is 6' in errors['clrn']

    msg.clrn = '123456'
    assert not msg.get_errors()

    root = msg.generate_xml()
    msg.validate_xml(root)
