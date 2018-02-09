import xmlschema

from fp17.bcds1 import generate_bcds1

XSD_FILENAME = 'xsd/xml_bcds1.xsd'


def test_simple():
    xml = generate_bcds1()
    schema = xmlschema.XMLSchema(XSD_FILENAME)

    schema.validate(xml)
