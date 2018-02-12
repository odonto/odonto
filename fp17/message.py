import os
import xmlschema


class Message(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._errors = {}  # (str, None) -> [str]

    def add_error(self, field, error):
        self._errors.setdefault(field, []).extend(error)

    @property
    def errors(self):
        if not self._errors:
            self.clean()
        return self._errors

    def full_clean(self):
        self._errors = {}

    def is_valid(self):
        return not bool(self.errors)

    @classmethod
    def validate_xml(cls, root):
        schema = xmlschema.XMLSchema(os.path.join('xsd', cls.Meta.schema))

        schema.validate(root)
