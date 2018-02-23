import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
import gc
import os
import time
from glob import glob
import re
from pprint import pprint

import datacube
from datacube.storage.storage import write_dataset_to_netcdf
import dask
import dask.multiprocessing
from dask.diagnostics import ProgressBar
# dask.set_options(get=dask.multiprocessing.get)

# Nc files
sr_file = '/tmp/sr.nc'
sr_out_uncompressed = '/tmp/sr_reduce_uncompressed.nc'
sr_out_compressed = '/tmp/sr_reduce_compressed.nc'
sr_out_xr = '/tmp/sr_out_xr.nc'

# Delete all output files
def delete_if_exists(x):
    if os.path.isfile(x):
        os.remove(x)

[delete_if_exists(x) for x in [sr_out_uncompressed, sr_out_compressed, sr_out_xr]]

# List to store timing results
timing = []

# Datacube session
dc = datacube.Datacube(app = 'dc_benchmark')

# load params
dc_param = {'x': (-105, -103),
            'y': (19, 21),
            'time': (datetime(2017, 1, 1), datetime(2017, 12, 31)),
            'dask_chunks': {'x': 2000, 'y': 2000},
            'measurements': ['blue', 'green', 'red', 'nir', 'swir1', 'swir2'],
           }

# LIsts of storage units
list_compressed = glob('/home/madmex_user/datacube_ingest/LS8_espa/mexico/*.nc')
list_uncompressed = glob('/home/madmex_user/datacube_ingest/LS8_espa_uncompressed/mexico/*.nc')

# Filter lists
pattern = re.compile(r'.*LS8_espa_1[45]_-1[45]_2017.*\.nc$')
list_compressed_filtered = [x for x in list_compressed if pattern.match(x)]
list_uncompressed_filtered = [x for x in list_uncompressed if pattern.match(x)]
pprint(list_compressed_filtered)

############
# First test: Load from datacube uncompressed collection
############
# print('Begin first test\n')
# time_begin = time.time()
# sr = dc.load(product='ls8_espa_mexico_uncompressed', **dc_param)
# sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
# sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
# sr_mean.rename({'blue': 'blue_mean',
#                 'green': 'green_mean',
#                 'red': 'red_mean',
#                 'nir': 'nir_mean',
#                 'swir1': 'swir1_mean',
#                 'swir2': 'swir2_mean',
#                 'ndvi': 'ndvi_mean'}, inplace=True)
# sr_mean.attrs['crs'] = sr.attrs['crs']
# print(sr_mean)
# write_dataset_to_netcdf(sr_mean, sr_out_uncompressed)
# time_end = time.time()
# timing.append(time_end - time_begin)


############
# Second test: Load from storage units using xarray
############
print('Begin second test\n')
time_begin = time.time()
sr = xr.open_mfdataset(list_uncompressed_filtered, chunks = {'x': 2000, 'y': 2000},
                       concat_dim = ['time', 'x', 'y'],
                       data_vars = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2'],
                       drop_variables=['pixel_qa'])
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
print(sr)
print(sr_mean)
sr_mean.to_netcdf(sr_out_xr)
time_end = time.time()
timing.append(time_end - time_begin)


# summary
for id, t in enumerate(timing):
    print('Test %d completed in %.1f seconds' % (id, t))
