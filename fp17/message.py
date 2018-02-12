import os
import xmlschema


class Message(object):
    SCHEMA = None

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.SCHEMA))

        schema.validate(root)
