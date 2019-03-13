"""
Message envelope
----------------
"""

import pkg_resources

from lxml import etree

from .utils import min_digits, max_digits, strbool
from .message import Message


try:
    VERSION = pkg_resources.require('fp17').version
except pkg_resources.DistributionNotFound:
    VERSION = 'unknown'


class Envelope(Message):
    def __init__(self):
        super().__init__()

        self._messages = []

    def add_message(self, message):
        self._messages.append(message)

    class Meta:
        xsd = 'xml_envelope.xsd'

        schema = {
            # Serial number
            #
            # Sequential, unique number from site for each interchange.
            'serial_number': {
                'type': 'number',
                'min': min_digits(0),
                'max': max_digits(6),
                'required': True,
            },

            # Destination
            #
            # For messages orginated by the system, the unique five digit site
            # number issued by the service. Messages originated by a user use
            # the code appropriate to the service.
            'destination': {
                'type': 'string',
                'required': True,
                'required': True,
                'minlength': 1,
                'maxlength': 35,
            },

            # Date of release of interchange for transmission
            'release_timestamp': {
                'type': 'datetime',
                'required': True,
            },

            # Origin
            #
            # For messages orginated by the user, the unique five digit site
            # number issued by the system. Messages originated by the system
            # use the code appropriate to the service.
            'origin': {
                'type': 'string',
                'required': True,
                'minlength': 1,
                'maxlength': 35,
            },

            # Practice system approval number
            'approval_number': {
                'type': 'number',
                'min': min_digits(0),
                'max': max_digits(6),
                'required': True,
            },

            # Revision level
            'revision_level': {
                'type': 'number',
                'allowed': (1,),
                'required': False,
            },

            # Transmission category
            'transmission_category': {
                'type': 'number',
                'allowed': (1, 2, 3),
                'required': False,
            },

            # Test indicator
            'test': {
                'type': 'boolean',
                'required': False,
            },

            # Interchange control count.
            #
            # Number of messages in the interchange. Required for interchanges
            # in the END service.
            'interchange_control_count': {
                'type': 'number',
                'min': 0,
                'max': 999999,
                'required': False,
            },

            # Practice system software package version
            'software_name': {
                'type': 'string',
                'default': 'pythonfp17',
                'regex': '^[a-zA-Z0-9]{1,50}$',
                'required': True,
            },

            # Practice system software package version
            'software_version': {
                'type': 'string',
                'default': VERSION,
                'regex': '^[a-zA-Z0-9]{1,50}$',
                'required': True,
            },
        }

    @staticmethod
    def get_root_xml_element(x):
        root = etree.Element('ic')

        root.attrib['schvn'] = '1.0'
        root.attrib['synv'] = '1'
        root.attrib['ori'] = x['origin']
        root.attrib['dest'] = x['destination']
        root.attrib['datrel'] = x['release_timestamp'].strftime('%y%m%d')
        root.attrib['tim'] = x['release_timestamp'].strftime('%H%M')
        root.attrib['seq'] = '{:06d}'.format(x['serial_number'])
        root.attrib['swname'] = x['software_name']
        root.attrib['swver'] = x['software_version']
        root.attrib['pmsno'] = '{:08d}'.format(x['approval_number'])

        for k, v, fn in (
            ('icct', 'interchange_control_count', str),
            ('rev', 'revision_level', str),
            ('xmcat', 'transmission_category', str),
            ('teind', 'test', strbool),
        ):
            try:
                root.attrib[k] = fn(x[v])
            except KeyError:
                pass

        return root

    def generate_xml(self):
        elem = super().generate_xml()

        for x in self._messages:
            elem.append(x.generate_xml())

        return elem
