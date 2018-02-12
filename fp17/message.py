import os
import inspect
import xmlschema

from .exc import ValidationError


class Field(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value):
        pass


class Message(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fields = inspect.getmembers(self, lambda x: isinstance(x, Field))
        self._errors = None

        self.data = {}

    def add_error(self, field, error):
        self._errors.setdefault(field, []).append(error)

    def set_value(self, field, value):
        self.data[field] = value
        self._errors = None

    @property
    def errors(self):
        if self._errors is None:
            self._errors = {}
            for k, v in self._fields:
                try:
                     v.validate(self.data[k])
                except ValidationError as exc:
                    self.add_error(k, exc.message)
                except KeyError:
                    self.add_error(k, "Missing field '{}'".format(k))

        return self._errors

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.schema))
        schema.validate(root)
