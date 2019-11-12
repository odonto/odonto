import os
import inspect
import cerberus
import datetime
import xmlschema
from django.conf import settings


class Message(object):
    Validator = cerberus.Validator

    def __init__(self, **kwargs):
        super().__init__()

        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def generate_root(msg):
        raise NotImplementedError()

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join(
            settings.PROJECT_PATH, 'odonto_submissions', 'xsd', cls.Meta.xsd
        ))

        schema.validate(root)

    def get_errors(self):
        return self.get_validator().errors

    def get_validator(self):
        x = self.Validator(self.Meta.schema)
        x.validate(flatten(self))
        return x

    def generate_xml(self):
        x = self.get_validator()

        return self.get_root_xml_element(x.document)


def flatten(val):
    if isinstance(val, dict):
        return {
            k: flatten(v) for k, v in val.items() if not k.startswith('_')
        }
    if isinstance(val, list):
        return [flatten(x) for x in val]
    if isinstance(val, (int, str, datetime.datetime, datetime.date)):
        return val
    return flatten(val.__dict__)
