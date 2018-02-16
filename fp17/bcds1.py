from lxml import etree

from .message import Message


class BCDS1Message(Message):
    class Meta:
        schema = {
            # Message reference number
            #
            # Sequential number assigned by the practice application that
            # within contract number (9105) uniquely identifies a message.
            'message_reference_number': {
                'type': 'number',
                'min': 100000,
                'max': 999999,
                'required': True,
            },

            # Performer number
            #
            # Performer number issued by NHSDS.  This will be existing personal
            # number if the dentist has already been issued with one.
            'performer_number': {
                'type': 'number',
                'min': 100000,
                'max': 999999,
                'required': True,
            },
        }
        xsd_schema = 'xml_bcds1.xsd'

    def generate_xml(self):
        root = etree.Element('bcds1')

        root.attrib['schvn'] = '1.0'

        root.attrib['clrn'] = str(self.message_reference_number)
        root.attrib['perf'] = str(self.performer_number)

        root.attrib['pin'] = '123456'
        root.attrib['cno'] = '1234567890'
        root.attrib['noseg'] = '5'
        root.attrib['loc'] = '123456'
        root.attrib['resct'] = '99'

        pat = etree.SubElement(root, 'pat')
        pat.attrib['sex'] = 'M'
        pat.attrib['dob'] = '19991231'  # YYYYMMDD
        pat.attrib['ptttl'] = 'Mr'
        pat.attrib['ptfn'] = 'John'
        pat.attrib['ptsur'] = 'Smith'
        pat.attrib['prvsur'] = 'Smythe'  # previous
        pat.attrib['nhsno'] = '1234'
        pat.attrib['nino'] = '123456789'
        adrdet = etree.SubElement(pat, 'adrdet')
        for x in range(5):
            adrln = etree.SubElement(adrdet, 'adrln')
            adrln.text = 'Address {}'.format(x)

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
