import datetime

from lxml import etree

from fp17.bcds1 import BCDS1, Patient, Treatment, SCHEDULE_QUERY_TRUE
from fp17.envelope import Envelope

"""
FIXME:
#Treatment Category	Clinical Data Set
    #   Band 1	Examination (9317), Recall Interval (9172 9), Scale & Polish, Ethnic Origin 1
"""

def generate():
    bcds1 = BCDS1()
    bcds1.message_reference_number = 123456
    bcds1.performer_number = 123456
    bcds1.dpb_pin = 123456
    bcds1.contract_number = 1234567890
    bcds1.location = 123456

    bcds1.patient = Patient()
    bcds1.patient.surname = "Barlaston"
    bcds1.patient.forename = "Sally"
    bcds1.patient.address = ["1 High Street"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1958, 1, 23)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060
    bcds1.patient_charge_currency = 'GBP'

    treatment = Treatment()
    treatment.code = 9150
    treatment.instance_count = 1
    bcds1.treatments = [treatment]

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

    return root

if __name__ == '__main__':
    root = generate()
    print(etree.tostring(root, encoding='unicode', pretty_print=True).strip())
