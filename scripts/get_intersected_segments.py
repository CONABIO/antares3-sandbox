#!/usr/bin/env python3.6

"""
# Usage
./get_intersected_segments.py polygons_filenames_list.txt crops_points_file.shp results_directory
"""

import fiona
from shapely.geometry import mapping, shape
import os
import sys
from fiona.crs import to_string

polygonslistfile = sys.argv[1]
pointsfile = sys.argv[2]
directory = sys.argv[3]

with open(polygonslistfile, 'r') as f:
    polygonfileslist = f.read().splitlines()

with fiona.open(pointsfile) as src:
    ptfc = list(src)

ptfcn = [{'type': 'feature',
                   'geometry': mapping(shape(pt['geometry'])),
                   'properties': {'id': i,
                                  'cultivo': pt['properties']['Name']}} for i, pt in enumerate(ptfc)]


poly_fc = []
points_fc = []

for index in range(len(polygonfileslist)):
    with fiona.open(polygonfileslist[index]) as src:
        crs_str = to_string(src.crs)
        pyfc = list(src)

    # Build the feature collection
    fc=[{'type': 'feature',
                   'geometry': mapping(shape(py['geometry'])),
                   'properties': {'features_i': py['properties']['features_i'],
                                  'cultivo': pt['properties']['cultivo'],
                                  'preds': py['properties']['preds']}} for pt in ptfcn for py in pyfc if shape(py['geometry']).intersects(shape(pt['geometry'])) ]

    schema = {'geometry': 'Polygon',
                      'properties': {'features_i': 'int',
                                     'cultivo': 'str',
                                     'preds': 'int'}}


    pyfc=[]

    with fiona.open('{}/{}'.format(directory,polygonfileslist[index].split('/')[-1]), 'w', schema=schema, crs=crs_str,
                    driver='ESRI Shapefile') as dst:
        for row in fc:
            dst.write(row)
    fc=[]
