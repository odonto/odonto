import os
import inspect
import cerberus
import xmlschema


class Message(object):
    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.xsd_schema))

        schema.validate(root)

    def get_errors(self):
        x = cerberus.Validator(self.Meta.schema)
        x.validate(self.__dict__)

        return x.errors
