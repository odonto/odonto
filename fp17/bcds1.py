from lxml import etree

from .utils import min_digits, max_digits
from .message import Message
from .patient import Patient


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
        adrdet.attrib['pc'] = 'N1 1AA'
        for idx in range(5):
            adrln = etree.SubElement(adrdet, 'adrln')
            adrln.text = 'Address {}'.format(idx)

        tda = etree.SubElement(root, 'tda')
        tda.attrib['dtdec'] = '67'
        tda.attrib['sqind'] = '3'
        trtdatgrp = etree.SubElement(tda, 'trtdatgrp')
        trtdatgrp.attrib['datacc'] = '991231'  # acceptance (YYMMDD)
        trtdatgrp.attrib['datcp'] = '991231'  # completion (YYMMDD)
        trtdatgrp.attrib['datexm'] = '991231'  # examination (YYMMDD)
        clty = etree.SubElement(tda, 'clty')
        clty.attrib['inireg'] = 'false'
        clty.attrib['rereg'] = 'false'
        clty.attrib['ptothdt'] = 'false'
        clty.attrib['octrt'] = 'false'
        clty.attrib['trtrfl'] = 'false'
        clty.attrib['nhspri'] = 'false'
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
