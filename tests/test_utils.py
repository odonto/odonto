from fp17.utils import min_digits, max_digits, strbool


def test_min_digits():
    assert min_digits(0) == 0
    assert min_digits(1) == 1
    assert min_digits(6) == 100000


def test_max_digits():
    assert max_digits(0) == 0
    assert max_digits(1) == 9
    assert max_digits(6) == 999999


def test_strbool():
    assert strbool(True) == 'true'
    assert strbool(False) == 'false'

    assert strbool([]) == 'false'
    assert strbool([1]) == 'true'
