from mapkick.flask import Map, AreaMap
import pytest


class TestFlask:
    def test_map(self):
        map = Map([{'latitude': 37.7829, 'longitude': -122.4190}])
        assert 'new Mapkick' in str(map)

    def test_area_map(self):
        map = AreaMap([])
        assert 'new Mapkick' in str(map)

    def test_escape_data(self):
        map = Map('</script><script>alert("xss")</script>')
        assert '\\u003cscript\\u003e' in str(map)
        assert '<script>alert' not in str(map)

    def test_escape_options(self):
        map = Map([], xss='</script><script>alert("xss")</script>')
        assert '\\u003cscript\\u003e' in str(map)
        assert '<script>alert' not in str(map)

    def test_height_pixels(self):
        assert 'height: 100px;' in str(Map([], height='100px'))

    def test_height_percent(self):
        assert 'height: 100%;' in str(Map([], height='100%'))

    def test_height_dot(self):
        assert 'height: 2.5rem;' in str(Map([], height='2.5rem'))

    def test_height_quote(self):
        with pytest.raises(ValueError) as excinfo:
            Map([], height='150px"')
        assert 'Invalid height' in str(excinfo.value)

    def test_height_semicolon(self):
        with pytest.raises(ValueError) as excinfo:
            Map([], height='150px;background:123')
        assert 'Invalid height' in str(excinfo.value)

    def test_width_pixels(self):
        assert 'width: 100px;' in str(Map([], width='100px'))

    def test_width_percent(self):
        assert 'width: 100%;' in str(Map([], width='100%'))

    def test_width_dot(self):
        assert 'width: 2.5rem;' in str(Map([], width='2.5rem'))

    def test_width_quote(self):
        with pytest.raises(ValueError) as excinfo:
            Map([], width='80%"')
        assert 'Invalid width' in str(excinfo.value)

    def test_width_semicolon(self):
        with pytest.raises(ValueError) as excinfo:
            Map([], width='80%;background:123')
        assert 'Invalid width' in str(excinfo.value)

    def test_loading(self):
        assert '>Loading!!</div>' in str(Map([], loading='Loading!!'))

    def test_loading_escaped(self):
        assert '&lt;b&gt;Loading!!&lt;/b&gt;' in str(Map([], loading='<b>Loading!!</b>'))
        assert '<b>' not in str(Map([], loading='<b>Loading!!</b>'))

    def test_secret_token(self):
        with pytest.raises(ValueError) as excinfo:
            Map([], access_token='sk.token')
        assert 'Expected public access token' in str(excinfo.value)

    def test_invalid_token(self):
        with pytest.raises(ValueError) as excinfo:
            Map([], access_token='token')
        assert 'Invalid access token' in str(excinfo.value)

    def test_no_token(self):
        assert 'accessToken' not in str(Map([]))
