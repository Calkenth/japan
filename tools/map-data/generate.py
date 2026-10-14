"""Generator danych mapy (linia brzegowa i jeziora) dla index.html.

Pobiera Natural Earth 1:10m, przycina do zasięgu mapy, upraszcza i wypisuje JSON
do wklejenia w index.html jako window.__MAP__ = {...};

Użycie:
    pip install shapely
    python3 tools/map-data/generate.py > map.json
"""
import json
import math
import sys
import urllib.request

from shapely.geometry import box, shape

BASE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'

# Zasięg całych danych (z marginesem, żeby przycięte krawędzie lądu nie były widoczne)
LON0, LON1, LAT0, LAT1 = 133.5, 141.6, 33.4, 37.85
# Obszar, poza który nie da się przesunąć widoku: [lon min, lat min, lon max, lat max]
INNER = [134.0, 33.9, 141.1, 37.35]

# Rzut równoodległościowy w kilometrach, skalowany na szerokości 35,6°
KX = math.cos(math.radians(35.6)) * 111.32
KY = 110.57
# Uproszczenie linii w stopniach
LAND_TOLERANCE = 0.002
LAKE_TOLERANCE = 0.003


def project(lon, lat):
    return (lon - LON0) * KX, (LAT1 - lat) * KY


def load(name, min_area):
    with urllib.request.urlopen(BASE + name) as r:
        features = json.load(r)['features']
    area = box(LON0, LAT0, LON1, LAT1)
    polygons = []
    for f in features:
        geom = shape(f['geometry'])
        if not geom.intersects(area):
            continue
        clipped = geom.intersection(area)
        parts = [clipped] if clipped.geom_type == 'Polygon' else list(getattr(clipped, 'geoms', []))
        polygons += [p for p in parts if p.geom_type == 'Polygon' and p.area >= min_area]
    return polygons


def to_path(polygons, tolerance):
    out = []
    for p in polygons:
        simple = p.simplify(tolerance, preserve_topology=True)
        for ring in [simple.exterior, *simple.interiors]:
            pts = [project(*c) for c in ring.coords]
            if len(pts) < 4:
                continue
            out.append('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts[:-1]) + 'Z')
    return ''.join(out)


def main():
    data = {
        'lon0': LON0,
        'lat1': LAT1,
        'inner': INNER,
        'land': to_path(load('ne_10m_land.geojson', 0.0005), LAND_TOLERANCE),
        'lakes': to_path(load('ne_10m_lakes.geojson', 0.002), LAKE_TOLERANCE),
    }
    json.dump(data, sys.stdout, separators=(',', ':'))


if __name__ == '__main__':
    main()
