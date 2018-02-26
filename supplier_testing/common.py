import datetime

from lxml import etree

from fp17.bcds1 import BCDS1, Patient
from fp17.envelope import Envelope


def get_base():
    bcds1 = BCDS1()
    bcds1.message_reference_number = 123456
    bcds1.performer_number = 123456
    bcds1.dpb_pin = 123456
    bcds1.contract_number = 1234567890
    bcds1.location = 123456

    bcds1.patient = Patient()

    return bcds1


def output(bcds1):
    assert not bcds1.get_errors(), bcds1.get_errors()

    BCDS1.validate_xml(bcds1.generate_xml())

    envelope = Envelope()
    envelope.origin = "1234"
    envelope.destination = "1234"
    envelope.release_timestamp = datetime.datetime.utcnow()
    envelope.test = True
    envelope.serial_number = 1
    envelope.add_message(bcds1)

    assert not envelope.get_errors(), envelope.get_errors()

    root = envelope.generate_xml()
    Envelope.validate_xml(root)

    print(etree.tostring(root, encoding='unicode', pretty_print=True).strip())
