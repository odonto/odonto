import os
import xmlschema


class Message(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._errors = None

    def full_clean(self):
        self._errors = []

    @property
    def errors(self):
        if self._errors is None:
            self.full_clean()
        return self._errors

    def is_valid(self):
        return not bool(self._errors)

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.schema))

        schema.validate(root)
