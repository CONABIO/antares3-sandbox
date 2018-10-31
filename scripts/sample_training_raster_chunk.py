#!/usr/bin/env python3
"""
# Usage
./sample_training_raster_chunk.py input_raster.tif output_dir 1000 50 2000

First argument: input categorical raster
Second argument: output directory where 1 shapefile per chunk will be written
Third argument: Number of samples per chunk
Fourth argument: radius of each circular sample in CRS unit
Fifth argument: chunk size in number of pixel

Note: zero is assumed to be no-data, update the code if that's not the case
"""
import random
import sys
import itertools
import os

import rasterio
import rasterio.features
from rasterio.windows import Window
from shapely.geometry import Point, mapping
import numpy as np
import fiona


r = sys.argv[1]
out_dir = sys.argv[2]
n_sample = int(sys.argv[3])
buffer_size = float(sys.argv[4])
chunk_size = int(sys.argv[5])


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


def chunk_dim(length, chunk_size):
    begins = range(0, length, chunk_size)
    n_complete, remain = divmod(length, chunk_size)
    intervals = list(itertools.repeat(chunk_size, n_complete)) + [remain]
    return zip(begins, intervals)


def window_generator(dataset, chunk_size):
    """Generator of (window index, window)"""
    for i, col in enumerate(chunk_dim(dataset.width, chunk_size)):
        for j, row in enumerate(chunk_dim(dataset.height, chunk_size)):
            yield ((j, i), Window(col[0], row[0], col[1], row[1]))


if __name__ == "__main__":
    with rasterio.open(r) as src:
        for win in window_generator(src, chunk_size):
            min_x, min_y, max_x, max_y = rasterio.windows.bounds(win[1],
                                                               src.transform)
            train_arr = src.read(1, window=win[1])
            aff = rasterio.windows.transform(win[1], src.transform)
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

            # Build output filename
            out_file = os.path.join(out_dir, '%d_%d_training.shp' % win[0])

            with fiona.open(out_file, 'w', schema=schema, crs=crs,
                            driver='ESRI Shapefile') as dst:
                for row in fc:
                    dst.write(row)






