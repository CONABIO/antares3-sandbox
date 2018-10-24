#!/usr/bin/env python3
import random
import sys

import rasterio
import rasterio.features
from shapely.geometry import Point, mapping
import numpy as np
import fiona

# ./sample_training_raster.py input_raster.tif output_shapefile.shp 10000 0.0005

r = sys.argv[1]
out_file = sys.argv[2]
n_sample = int(sys.argv[3])
buffer_size = float(sys.argv[4])


def groupby(x, g):
    """Split a 2D array along the zero dimension using an array of groups

    Args:
        x (np.ndarray): 1D array of values
        g (np.ndarray): 1D Array of groups

    Return:
        zip: Generator of (group, np.ndarray) tupples. The second element correspond
        to the split x array
    """
    sidg = g.argsort(kind='mergesort')
    g_sorted = g[sidg]
    x_sorted = x[sidg]
    x_out = np.split(x_sorted, np.flatnonzero(g_sorted[1:] != g_sorted[:-1])+1)
    return zip(np.unique(g), x_out)


if __name__ == "__main__":
    with rasterio.open(r) as src:
        min_x, min_y, max_x, max_y = src.bounds
        train_arr = src.read(1)
        aff = src.transform
        crs = src.crs

    # Generate random points
    points = [Point([random.uniform(min_x, max_x),
                     random.uniform(min_y, max_y)]) for x in range(n_sample)]

    # Build polygons from points
    polygons = [x.buffer(buffer_size) for x in points]

    # Rasterize sample polygons
    samples_arr = rasterio.features.rasterize(zip(polygons, range(n_sample)),
                                              out_shape=train_arr.shape,
                                              transform=aff,
                                              fill=-1)

    # Extract values of train-arr using samples_arr
    train_arr = train_arr[samples_arr != -1].flatten()
    samples_arr = samples_arr[samples_arr != -1].flatten()
    grouped_arrs = groupby(train_arr, samples_arr)
    aggregated = [(x[0], np.unique(x[1])) for x in grouped_arrs]

    # Filter non pure polygons
    aggregated = [(x[0], int(x[1])) for x in aggregated if len(x[1]) == 1]
    # Filter class 0
    aggregated = [x for x in aggregated if x[1] != 0]
    # Build the feature collection
    fc = [{'type': 'feature',
           'geometry': mapping(polygons[x[0]]),
           'properties': {'class': x[1]}}
          for x in aggregated]

    schema = {'geometry': 'Polygon',
              'properties': {'class': 'int'}}

    with fiona.open(out_file, 'w', schema=schema, crs=crs,
                    driver='ESRI Shapefile') as dst:
        for row in fc:
            dst.write(row)






