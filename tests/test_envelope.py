import pytest

from fp17.envelope import Envelope


@pytest.fixture
def envelope():
    msg = Envelope()
    msg.origin = '01009'

    return msg


def test_valid(envelope):
    v = envelope.get_validator()

    assert not v.errors

    root = envelope.generate_xml()

    Envelope.validate_xml(root)


def test_validation():
    msg = Envelope()

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
