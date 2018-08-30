import pytest
import datetime

from fp17.envelope import Envelope

from test_bcds1 import bcds1


@pytest.fixture
def envelope():
    msg = Envelope()
    msg.origin = '01009'
    msg.destination = '01009'
    msg.release_timestamp = datetime.datetime(1985, 12, 16, 16, 40)
    msg.serial_number = 0
    msg.approval_number = 16
    msg.revision_level = 1
    msg.transmission_category = 1
    msg.test = True
    msg.interchange_control_count = 2

    return msg


def test_valid(envelope):
    v = envelope.get_validator()

    assert not v.errors

    root = envelope.generate_xml()
    assert len(root.getchildren()) == 0

    Envelope.validate_xml(root)


def test_validation():
    msg = Envelope()

    errors = msg.get_errors()
    assert 'required field' in errors['origin']

    msg.origin = '01'
    errors = msg.get_errors()
    assert 'origin' not in errors


def test_add_message(envelope, bcds1):
    envelope.add_message(bcds1)
    root = envelope.generate_xml()
    children = root.getchildren()

    assert len(children) == 1
    assert children[0].tag == 'bcds1'

    envelope.validate_xml(root)
