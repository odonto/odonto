import os
import inspect
import cerberus
import xmlschema


class Message(object):
    @staticmethod
    def generate_xml(msg):
        raise NotImplementedError()

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.xsd_schema))

        schema.validate(root)

    def get_errors(self):
        return self.get_validator().errors

    def get_validator(self):
        x = cerberus.Validator(self.Meta.schema)
        x.validate(self.__dict__)

        return x
