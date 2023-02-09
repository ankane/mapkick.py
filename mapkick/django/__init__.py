from django.utils.html import format_html, json_script, mark_safe
import os
import re
import secrets


class BaseMap:
    def __init__(self, type, data, **options):
        # important! check escaping before making configurable
        element_id = 'map-' + secrets.token_hex(16)
        json_element_id = element_id + '-json'

        height = str(options.pop('height', '500px'))
        width = str(options.pop('width', '100%'))

        for (k, v) in [('height', height), ('width', width)]:
            # limit to alphanumeric and % for simplicity
            # this prevents things like calc() but safety is the priority
            # dot does not need escaped in square brackets
            if not re.match('^[a-zA-Z0-9%.]*$', v):
                raise ValueError('Invalid ' + k)

        html_vars = [
            element_id,
            height,
            width,
            height,
            height,
            options.get('loading', 'Loading...')
        ]
        html = format_html("""<div id="{}" style="height: {}; width: {};"><div style="height: {}; text-align: center; color: #999; line-height: {}; font-size: 14px; font-family: 'Lucida Grande', 'Lucida Sans Unicode', Verdana, Arial, Helvetica, sans-serif;">{}</div></div>""", *html_vars)

        access_token = options.pop('access_token', options.pop('accessToken', os.environ.get('MAPBOX_ACCESS_TOKEN')))
        if access_token is not None:
            if access_token.startswith('sk.'):
                raise ValueError('Expected public access token')
            elif not access_token.startswith('pk.'):
                raise ValueError('Invalid access token')
            options['accessToken'] = access_token

        js_vars = {
            'type': type,
            'id': element_id,
            'data': data,
            'options': options
        }
        json = json_script(js_vars, element_id=json_element_id)

        js = """<script>
  (function() {
    var createMap = function() {
      var o = JSON.parse(document.currentScript.previousElementSibling.textContent);
      new Mapkick[o.type](o.id, o.data, o.options);
    };
    if ("Mapkick" in window) {
      createMap();
    } else {
      window.addEventListener("mapkick:load", createMap, true);
    }
  })();
</script>"""

        self.__str = format_html('{}\n{}\n{}', mark_safe(html), json, mark_safe(js))

    def __str__(self):
        return self.__str


class Map(BaseMap):
    def __init__(self, data, **options):
        super().__init__('Map', data, **options)


class AreaMap(BaseMap):
    def __init__(self, data, **options):
        super().__init__('AreaMap', data, **options)
