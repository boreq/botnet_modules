from botnet_modules.lib import helpers


def test_get_md5():
    r = helpers.get_md5('test')
    assert type(r) is str
    assert r != ''
