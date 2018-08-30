from opal.core.test import OpalTestCase

import glob
import xmlschema


class ValidateXSDTestCase(OpalTestCase):
    def test_validate(self):
        for filename in glob.glob('xsd/*.xsd'):
            schema = xmlschema.XMLSchema(filename)

            self.failIf(schema.is_valid('<invalid/>'))

            with self.assertRaises(xmlschema.XMLSchemaValidationError):
                schema.validate('<invalid/>')
