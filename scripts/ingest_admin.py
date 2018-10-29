#!/usr/bin/env python3

"""Script to ingest mexico administrative boundaries from the file on conabio geoportal
instead of from GADM

Usage:
    ./ingest_admin.py /path/to/file.shp
"""

import json
from pprint import pprint
import sys

import fiona
from shapely.geometry import shape, mapping
from shapely.geometry import MultiPolygon as ShapelyMultiPolygon
from shapely.ops import cascaded_union
from django.contrib.gis.geos import GEOSGeometry

from madmex.models import Region, Country

if __name__ == "__main__":
    # Open file
    with fiona.open(sys.argv[1],
                    encoding='utf-8') as src:
        fc = list(src)

    # Build mex contours by merging all states and ingest it in db
    shape_list = [shape(feat['geometry']) for feat in fc]
    mex_shape = cascaded_union(shape_list)
    mex, _ = Country.objects.get_or_create(the_geom=GEOSGeometry(mex_shape.wkt, 4326),
                                           name='MEX')

    # Ingest states
    for feat in fc:
        name = feat['properties']['NOM_ENT']
        geom = ShapelyMultiPolygon([shape(feat['geometry'])])
        geom = GEOSGeometry(geom.wkt, 4326)
        _ = Region.objects.get_or_create(name=name,
                                         the_geom=geom,
                                         country=mex)
        print(name)
