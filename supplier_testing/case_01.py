import datetime

from fp17.bcds1 import BCDS1Message, Patient, Treatment, SCHEDULE_QUERY_TRUE

def generate():
    msg = BCDS1Message()
    msg.message_reference_number = 123456
    msg.performer_number = 123456
    msg.dpb_pin = 123456
    msg.contract_number = 1234567890
    msg.location = 123456

    msg.patient = Patient()
    msg.patient.surname = "Barlaston"
    msg.patient.forename = "Sally"
    msg.patient.address = ["1 High Street"]
    msg.patient.sex = 'F'
    msg.patient.date_of_birth = datetime.date(1958, 1, 23)

    msg.date_of_acceptance = datetime.date(2017, 4, 1)
    msg.date_of_completion = datetime.date(2017, 4, 1)

    msg.patient_charge_pence = 2060
    msg.patient_charge_currency = 'GBP'

    #Treatment Category	Clinical Data Set
    #   Band 1	Examination (9317), Recall Interval (9172 9), Scale & Polish, Ethnic Origin 1

    assert not msg.get_errors(), msg.get_errors()


    root = msg.generate_xml()
    BCDS1Message.validate_xml(root)

if __name__ == '__main__':
    generate()
