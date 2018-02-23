from lxml import etree

from .message import Message


class Envelope(Message):
    class Meta:
        xsd = 'xml_envelope.xsd'

        schema = {
            #
            'schvn': {
                'required': True,
            },

            #
            'synv': {
                'required': True,
            },

            #
            'seq': {
                'required': True,
            },

            #
            'dest': {
                'required': True,
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
            #

            'ori': {
                'required': True,
            },
        }

    @staticmethod
    def get_root_xml_element(x):
        root = etree.Element('ic')

        return root
