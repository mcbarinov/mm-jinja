from mm_jinja.filters import empty


def test_empty():
    assert empty(None) == ""
    assert empty("") == ""
    assert empty([]) == ""
    assert empty(0) == 0
