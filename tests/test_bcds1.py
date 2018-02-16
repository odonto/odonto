from fp17.bcds1 import BCDS1Message


def test_valid():
    msg = BCDS1Message()
    msg.message_reference_number = 123456
    msg.performer_number = 123456

    root = msg.generate_xml()
    msg.validate_xml(root)

def test_validation():
    msg = BCDS1Message()

    errors = msg.get_errors()
    assert 'required field' in errors['message_reference_number']

    msg.message_reference_number = 12345
    errors = msg.get_errors()
    assert 'min value is 100000' in errors['message_reference_number']

    msg.message_reference_number = 1234567
    errors = msg.get_errors()
    assert 'max value is 999999' in errors['message_reference_number']

    msg.message_reference_number = 123456
    assert 'clrn' not in msg.get_errors()

