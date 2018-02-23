import os
import inspect
import cerberus
import datetime
import xmlschema


class Message(object):
    @staticmethod
    def generate_root(msg):
        raise NotImplementedError()

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.xsd))

        schema.validate(root)

    def get_errors(self):
        return self.get_validator().errors

    def get_validator(self):
        x = cerberus.Validator(self.Meta.schema)
        x.validate({k: flatten(v) for k, v in self.__dict__.items()})

        return x

    def generate_xml(self):
        x = self.get_validator()

        return self.get_root_xml_element(x.document)


def flatten(val):
    if isinstance(val, dict):
        return val
    if isinstance(val, list):
        return [flatten(x) for x in val]
    if isinstance(val, (int, str, datetime.date, datetime.time)):
        return val
    return val.__dict__
