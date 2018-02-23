import pkg_resources

from lxml import etree

from .utils import min_digits, max_digits
from .message import Message


try:
    VERSION = pkg_resources.require('fp17').version
except pkg_resources.DistributionNotFound:
    VERSION = '(unknown)'


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
                'required': False,
            },

            # Practice system software package version
            'software_name': {
                'type': 'string',
                'default': 'python-fp17',
                'minlength': 1,
                'maxlength': 50,
                'required': True,
            },

            # Practice system software package version
            'software_version': {
                'type': 'string',
                'default': VERSION,
                'minlength': 1,
                'maxlength': 50,
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

        return root

    def generate_xml(self):
        elem = super().generate_xml()

        for x in self._messages:
            elem.append(x.generate_xml())

        return elem
