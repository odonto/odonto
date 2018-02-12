import os
import xmlschema


class Message(object):
    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.schema))

        schema.validate(root)
