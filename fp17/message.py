import os
import xmlschema
import collections


class Message(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._errors = None

        self.data = DataDict(self.Meta.fields)

    def add_error(self, field, error):
        self._errors.setdefault(field, []).append(error)

    @property
    def errors(self):
        if self._errors is None or self.data.modified:
            self._errors = {}

            for x in self.Meta.fields:
                if self.data[x] is None:
                    self.add_error(x, "Missing field '{}'".format(x))

        return self._errors

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.schema))

        schema.validate(root)


class DataDict(dict):
    def __init__(self, fields):
        self.data = {x: None for x in fields}
        self.modified = False

    def __getitem__(self, k):
        return self.data[k]

    def __setitem__(self, k, v):
        self.data[k] = v
        self.modified = True
