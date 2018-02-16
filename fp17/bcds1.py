from lxml import etree

from .utils import min_digits, max_digits
from .message import Message
from .patient import Patient

SCHEDULE_QUERY_TRUE = 0
SCHEDULE_QUERY_FALSE = 1
SCHEDULE_QUERY_DELETE = 3

class BCDS1Message(Message):
    class Meta:
        schema = {
            # Message reference number
            #
            # Sequential number assigned by the practice application that
            # within contract number (9105) uniquely identifies a message.
            'message_reference_number': {
                'type': 'number',
                'min': min_digits(6),
                'max': max_digits(6),
                'required': True,
            },

            # Performer number
            #
            # Performer number issued by NHSDS.  This will be existing personal
            # number if the dentist has already been issued with one.
            'performer_number': {
                'type': 'number',
                'min': min_digits(6),
                'max': max_digits(6),
                'required': True,
            },

            # DPB PIN
            #
            # Personal identification number assigned to a dentist by the NHSDS
            # used to authorise message transmission.
            'dpb_pin': {
                'type': 'number',
                'min': min_digits(6),
                'max': max_digits(6),
                'required': True,
            },

            # Contract number
            #
            # The provider’s unique contract number.
            'contract_number': {
                'type': 'number',
                'min': min_digits(10),
                'max': max_digits(15),
                'required': True,
            },

            # Location
            #
            # Unique code issued by NSHDS to show main location of address.
            'location': {
                'type': 'number',
                'min': min_digits(6),
                'max': max_digits(6),
                'required': True,
            },

            # Rebsubmission count
            #
            # Indicates that a claimhas been resubmitted to NHSDS following
            # amendment by the site. Increment by 1 for each resubmission.
            'resubmission_count': {
                'type': 'number',
                'min': 1,
                'max': 99,
                'default': 1,
                'required': False,
            },

            'patient': {
                'type': 'dict',
                'schema': Patient.Meta.schema,
                'required': True,
            },

            # Dentist / provider declaration
            #
            'provider_declaration': {
                'type': 'number',
                'allowed': (0, 1, 2, 3, 64, 65, 66, 67),
                'required': False,
            },

            # Schedule query
            'schedule_query': {
                'type': 'number',
                'allowed': (
                    SCHEDULE_QUERY_TRUE,
                    SCHEDULE_QUERY_FALSE,
                    SCHEDULE_QUERY_DELETE,
                ),
                'required': False,
            },

            # Date (of acceptance or registration)
            #
            'date_of_acceptance': {
                'type': 'date',
                'required': True,
            },

            # Date of completion
            #
            'date_of_completion': {
                'type': 'date',
                'required': False,
            },

            # Date of examination
            #
            'date_of_examination': {
                'type': 'date',
                'required': False,
            },

            # Types of claims
            #
            'types_of_claims': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        # Initial registration
                        #
                        'initial_registration': {
                            'type': 'boolean',
                            'required': True,
                        },

                        # Re-registration
                        #
                        'reregistration': {
                            'type': 'boolean',
                            'required': True,
                        },

                        # Patient under care of other dentist
                        #
                        'care_of_other_dentist': {
                            'type': 'boolean',
                            'required': True,
                        },

                        # Occasional treatment only
                        #
                        'occasional_treatment_only': {
                            'type': 'boolean',
                            'required': True,
                        },

                        # Treatment on referral
                        #
                        'treatment_on_referral': {
                            'type': 'boolean',
                            'required': True,
                        },

                        # Part NHS/private
                        #
                        'part_nhs_private': {
                            'type': 'boolean',
                            'required': True,
                        },
                    },
                },
                'default': [],
                'minlength': 0,
            },
        }

        xsd_schema = 'xml_bcds1.xsd'

    @staticmethod
    def get_root_xml_element(x):
        root = etree.Element('bcds1')

        root.attrib['schvn'] = '1.0'

        root.attrib['clrn'] = str(x['message_reference_number'])
        root.attrib['perf'] = str(x['performer_number'])
        root.attrib['pin'] = str(x['dpb_pin'])
        root.attrib['cno'] = str(x['contract_number'])
        root.attrib['loc'] = str(x['location'])
        root.attrib['resct'] = str(x['resubmission_count'])

        root.attrib['noseg'] = '5'  # calculated

        pat = etree.SubElement(root, 'pat')
        pat.attrib['sex'] = x['patient']['sex']
        pat.attrib['dob'] = x['patient']['date_of_birth'].strftime('%Y%m%d')
        pat.attrib['ptfn'] = x['patient']['forename']
        pat.attrib['ptsur'] = x['patient']['surname']

        for k, v in {
            'nino': 'national_insurance_number',
            'nhsno': 'nhs_number',
            'ptttl': 'title',
            'prvsur': 'previous_surname',
        }.items():
            if v in x['patient']:
                pat.attrib[k] = x['patient'][v]

        adrdet = etree.SubElement(pat, 'adrdet')
        for text in x['patient']['address']:
            adrln = etree.SubElement(adrdet, 'adrln')
            adrln.text = text
        if 'postcode' in x['patient']:
            adrdet.attrib['pc'] = x['patient']['postcode']

        tda = etree.SubElement(root, 'tda')
        for k, v in {
            'dtdec': 'provider_declaration',
            'sqind': 'schedule_query',
        }.items():
            if v in x:
                tda.attrib[k] = str(x[v])

        trtdatgrp = etree.SubElement(tda, 'trtdatgrp')
        for k, v in {
            'datacc': 'date_of_acceptance',
            'datcp': 'date_of_completion',
            'datexm': 'date_of_examination',
        }.items():
            if v in x:
                trtdatgrp.attrib[k] = x[v].strftime('%y%m%d')

        for vals in x['types_of_claims']:
            clty = etree.SubElement(tda, 'clty')
            for k, v in {
                'inireg': 'initial_registration',
                'rereg': 'reregistration',
                'ptothdt': 'care_of_other_dentist',
                'octrt': 'occasional_treatment_only',
                'trtrfl': 'treatment_on_referral',
                'nhspri': 'part_nhs_private',
            }.items():
                clty.attrib[k] = 'true' if vals[v] else 'false'

        trtarr = etree.SubElement(tda, 'trtarr')
        trtarr.attrib['cc18'] = 'false'
        trtarr.attrib['trttra'] = 'false'
        trtarr.attrib['radmod'] = 'false'
        trtarr.attrib['disfee'] = 'false'

        chx = etree.SubElement(root, 'chx')
        chx.attrib['ptchg'] = '100'
        chx.attrib['curcd'] = 'GBP'

        exrmdet = etree.SubElement(chx, 'exrmdet')
        exrmdet.attrib['exrmcd'] = '00'
        exrmdet.attrib['sdet'] = 'Supporting details'

        def create_reptrtty(parent):
            reptrtty = etree.SubElement(parent, 'reptrtty')
            reptrtty.attrib['trtcd'] = '1234'
            reptrtty.attrib['noins'] = '01'
            toid = etree.SubElement(reptrtty, 'toid')
            toid.text = '89'

        tst = etree.SubElement(root, 'tst')
        create_reptrtty(tst)

        cur = etree.SubElement(root, 'cur')
        create_reptrtty(cur)

        cht = etree.SubElement(root, 'cht')
        todata = etree.SubElement(cht, 'todata')
        todata.attrib['toid'] = '89'
        todata.attrib['ancd'] = 'BR'
        todata.attrib['xtvl'] = '01'

        return root
