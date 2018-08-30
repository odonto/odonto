import glob
import pytest
import xmlschema

XSD_FILES = glob.glob('xsd/*.xsd')


@pytest.mark.parametrize('filename', XSD_FILES)
def test_validate(filename):
    schema = xmlschema.XMLSchema(filename)

    assert not schema.is_valid('<invalid/>')

    with pytest.raises(xmlschema.XMLSchemaValidationError):
        schema.validate('<invalid/>')
