#!/usr/bin/env python3

"""
# Usage
./sample_training_polygons_rand_simple.py input_raster.tif output_dir 0.0001
First argument: input categorical raster
Second argument: output directory where 1 shapefile will be written
Third argument: fraction of dataset to be sampled. If -1 the total number of samples will be ~310000
"""

import rasterio
import rasterio.features
import fiona
from shapely.geometry import Point, mapping, shape
import numpy as np
from scipy import stats
from rasterio.windows import Window
import itertools
import os
import sys
from fiona.crs import to_string
import random
import traceback
import sys

r = sys.argv[1]
out_dir = sys.argv[2]
frac = float(sys.argv[3]) # 0.0001

def add_samples(frac, arr, train_arr, underep, fracu):
    mask = np.zeros(train_arr.size, dtype=np.uint8)
    for indx in np.where(arr)[0]:
        tmp = np.zeros(train_arr.shape, dtype=np.uint8)
        tmp[train_arr == indx+1] = 1
        ind = np.where(tmp.reshape(-1) == 1)[0]
        if underep:
            num = int(np.ceil(ind.size*fracu))
        else:
            num = int(np.ceil(ind.size*frac))  # 0.7/3600
        samples = np.array(random.sample(list(ind),num))
        mask[samples] = 1
    mask = mask.reshape(train_arr.shape)
    return mask

if __name__ == "__main__":
    with rasterio.open(r) as src:
          try:
            min_x, min_y, max_x, max_y = src.bounds
            train_arr = src.read(1)
            aff = src.transform
            crs_str = to_string(src.crs)

            # Build mask for shapes
            mask = np.zeros(train_arr.shape, dtype=np.uint8)

            # Count total number of pixels per class
            pxpcl = np.array([train_arr[train_arr == cl].size for cl in range(1,32)])

            if frac < 0:
                frac = 310000/np.sum(pxpcl)

            # Generate number of samples per class
            smplpxpcl = np.array([int(np.ceil(train_arr[train_arr == cl].size*frac)) for cl in range(1,32)])

            # Generate mask of samples
            smplcl = np.logical_and(pxpcl > 0, smplpxpcl > 0)
            if any(smplcl):
                mask[add_samples(frac, smplcl, train_arr, False, 0.5) == 1] = 1

            # Build the feature collection
            fc=[{'type': 'feature',
                   'geometry': mapping(shape(x[0])),
                   'properties': {'class': int(x[1])}} for x in rasterio.features.shapes(train_arr,mask,connectivity=8,transform=aff)]

            schema = {'geometry': 'Polygon',
                      'properties': {'class': 'int'}}

            # Build output filename
            out_file = os.path.join(out_dir, '{}_training.shp'.format(out_dir))

            with fiona.open(out_file, 'w', schema=schema, crs=crs_str,
                            driver='ESRI Shapefile') as dst:
                for row in fc:
                    dst.write(row)
            print('It contains {} polygons.'.format(len(fc)))
            print('number of pixels per class:')
            print('{}'.format(list(pxpcl)))
            print('number of sampled pixels per class:')
            print('{}'.format(list(smplpxpcl)))
          except Exception as e:
            print(e)
            traceback.print_exc()
            pass

