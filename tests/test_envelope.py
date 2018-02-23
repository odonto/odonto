import pytest
import datetime

from fp17.envelope import Envelope


@pytest.fixture
def envelope():
    msg = Envelope()
    msg.origin = '01009'
    msg.destination = '01009'
    msg.date_of_release = datetime.date(1985, 12, 16)
    msg.time_of_release = datetime.time(16, 40)

    return msg


def test_valid(envelope):
    v = envelope.get_validator()

    assert not v.errors

    root = envelope.generate_xml()

    Envelope.validate_xml(root)


def test_validation():
    msg = Envelope()

    errors = msg.get_errors()
    assert 'required field' in errors['origin']
