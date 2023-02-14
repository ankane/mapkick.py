# Mapkick.py

Create beautiful JavaScript maps with one line of Python. No more fighting with mapping libraries!

[See it in action](https://chartkick.com/mapkick-py)

For charts, check out [Chartkick.py](https://github.com/ankane/chartkick.py)

[![Build Status](https://github.com/ankane/mapkick.py/workflows/build/badge.svg?branch=master)](https://github.com/ankane/mapkick.py/actions)

## Installation

Run:

```sh
pip install mapkick
```

Mapkick uses [Mapbox GL JS v1](https://github.com/mapbox/mapbox-gl-js/tree/v1.13.3). To use tiles from Mapbox, [create a Mapbox account](https://account.mapbox.com/auth/signup/) to get an access token and set `MAPBOX_ACCESS_TOKEN` in your environment.

Then follow the instructions for your web framework:

- [Django](#django)
- [Flask](#flask) [unreleased]

### Django

Add to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    'mapkick.django',
    # ...
]
```

Load the JavaScript

```django
{% load static %}

<script src="{% static 'mapkick.bundle.js' %}"></script>
```

Create a map in a view

```python
from mapkick.django import Map

def index(request):
    map = Map([{'latitude': 37.7829, 'longitude': -122.4190}])
    return render(request, 'home/index.html', {'map': map})
```

And add it to the template

```django
{{ map }}
```

### Flask

Register the blueprint

```python
from mapkick.flask import mapkick

app.register_blueprint(mapkick)
```

Load the JavaScript

```jinja
<script src="{{ url_for('mapkick.static', filename='mapkick.bundle.js') }}"></script>
```

Create a map in a route

```python
from mapkick.flask import Map

def index():
    map = Map([{'latitude': 37.7829, 'longitude': -122.4190}])
    return render_template('home/index.html', map=map)
```

And add it to the template

```django
{{ map }}
```

## Maps

Point map

```python
Map([{'latitude': 37.7829, 'longitude': -122.4190}])
```

Area map (experimental)

```python
AreaMap([{'geometry': {'type': 'Polygon', 'coordinates': ...}}])
```

## Data

Data can be a list

```python
Map([{'latitude': 37.7829, 'longitude': -122.4190}])
```

Or a URL that returns JSON (same format as above)

```python
Map('/restaurants')
```

### Point Map

Use `latitude` or `lat` for latitude and `longitude`, `lon`, or `lng` for longitude

You can specify a label, tooltip, and color for each data point

```python
{
  'latitude': ...,
  'longitude': ...,
  'label': 'Hot Chicken Takeover',
  'tooltip': '5 stars',
  'color': '#f84d4d'
}
```

### Area Map

Use `geometry` with a GeoJSON `Polygon` or `MultiPolygon`

You can specify a label, tooltip, and color for each data point

```python
{
  'geometry': {'type': 'Polygon', 'coordinates': ...},
  'label': 'Hot Chicken Takeover',
  'tooltip': '5 stars',
  'color': '#0090ff'
}
```

## Options

Width and height

```python
Map(data, width='800px', height='500px')
```

Marker color

```python
Map(data, markers={'color': '#f84d4d'})
```

Show tooltips on click instead of hover

```python
Map(data, tooltips={'hover': False})
```

Allow HTML in tooltips (must sanitize manually)

```python
Map(data, tooltips={'html': True})
```

Map style

```python
Map(data, style='mapbox://styles/mapbox/outdoors-v12')
```

Zoom and controls

```python
Map(data, zoom=15, controls=True)
```

Refresh data from a remote source every `n` seconds

```python
Map(url, refresh=60)
```

## History

View the [changelog](https://github.com/ankane/mapkick.py/blob/master/CHANGELOG.md)

## Contributing

Everyone is encouraged to help improve this project. Here are a few ways you can help:

- [Report bugs](https://github.com/ankane/mapkick.py/issues)
- Fix bugs and [submit pull requests](https://github.com/ankane/mapkick.py/pulls)
- Write, clarify, or fix documentation
- Suggest or add new features

To get started with development:

```sh
git clone https://github.com/ankane/mapkick.py.git
cd mapkick.py
pip install -r requirements.txt
pytest
```
