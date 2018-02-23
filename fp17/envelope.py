from lxml import etree

from .message import Message


class Envelope(Message):
    class Meta:
        xsd = 'xml_envelope.xsd'

        schema = {
            #
            'seq': {
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

            #
            'swname': {
                'required': True,
            },

            #
            'datrel': {
                'required': True,
            },

            #
            'swver': {
                'required': True,
            },

            #
            'tim': {
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
        }

    @staticmethod
    def get_root_xml_element(x):
        root = etree.Element('ic')

        root.attrib['schvn'] = '1.0'
        root.attrib['synv'] = '1'
        root.attrib['ori'] = x['origin']
        root.attrib['dest'] = x['destination']

        return root
