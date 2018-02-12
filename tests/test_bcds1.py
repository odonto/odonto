from fp17.bcds1 import BCDS1Message


def test_simple():
    msg = BCDS1Message()
    assert not msg.is_valid()
    root = msg.generate_xml()
    BCDS1Message.validate_xml(root)
