import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
import gc
import os
import time

import datacube
from datacube.storage.storage import write_dataset_to_netcdf
import dask
import dask.multiprocessing
from dask.diagnostics import ProgressBar
# dask.set_options(get=dask.get)

# Nc files
sr_file = '/tmp/sr.nc'
sr_out_xarray = '/tmp/sr_reduce_xarray.nc'
sr_out_xarray_dask = '/tmp/sr_reduce_xarray_dask.nc'
sr_out_dc = '/tmp/sr_reduce_dc.nc'
sr_out_dc_dask = '/tmp/sr_reduce_dc_dask.nc'

# Delete all output files
def delete_if_exists(x):
    if os.path.isfile(x):
        os.remove(x)

[delete_if_exists(x) for x in [sr_out_xarray, sr_out_xarray_dask, sr_out_dc, sr_out_dc_dask]]

# List to store timing results
timing = []

# Generate Landsat time-series like nc file
if not os.path.isfile(sr_file):
    arr = np.random.randint(0, 10000, size=(20, 6000, 6000), dtype=np.int16)
    date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(20)]
    xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list})
    sr = xr.Dataset({'blue': xarr, 'green': xarr, 'red': xarr, 'nir': xarr * 2,
                     'swir1': xarr, 'swir2': xarr})
    sr.to_netcdf('/tmp/sr.nc')
    sr = None
    xarr = None
    gc.collect()

############
# First test: single thread processing from netcdf
############
print('Begin first test\n')
time_begin = time.time()
sr = xr.open_dataset(sr_file)
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
sr_min = sr.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
sr_max = sr.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
sr_std = sr.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
# Merge dataarrays
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
print(combined)
combined.to_netcdf(sr_out_xarray)
time_end = time.time()
timing.append(time_end - time_begin)

############
# Second test: Dask with 20 cores from netcdf
############
print('Begin second test\n')
time_begin = time.time()
sr = xr.open_dataset(sr_file,
                     chunks={'x': 2000, 'y': 2000})
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
sr_min = sr.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
sr_max = sr.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
sr_std = sr.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
# Merge dataarrays
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
print(combined)
combined.to_netcdf(sr_out_xarray_dask)
time_end = time.time()
timing.append(time_end - time_begin)

############
# Third test: datacube single thread
############
print('Begin third test\n')
time_begin = time.time()
dc = datacube.Datacube(app = 'dc_benchmark')
sr = dc.load(product='ls8_espa_mexico', x=(-104, -103), y=(20, 21),
             time=(datetime(2017, 1, 1), datetime(2017, 12, 31)), group_by='solar_day',
             measurements=['blue', 'green', 'red', 'nir', 'swir1', 'swir2'])
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
sr_min = sr.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
sr_max = sr.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
sr_std = sr.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
combined.attrs['crs'] = sr.attrs['crs']
print(combined)
write_dataset_to_netcdf(combined, sr_out_dc)
time_end = time.time()
timing.append(time_end - time_begin)

############
# Fourth test: datacube  with dask 20 cores
############
print('Begin fourth test\n')
time_begin = time.time()
dc = datacube.Datacube(app = 'dc_dask_benchmark')
sr = dc.load(product='ls8_espa_mexico', x=(-104, -103), y=(20, 21),
               time=(datetime(2017, 1, 1), datetime(2017, 12, 31)), group_by='solar_day',
               measurements=['blue', 'green', 'red', 'nir', 'swir1', 'swir2'],
               dask_chunks={'x': 2000, 'y': 2000})
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
sr_min = sr.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
sr_max = sr.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
sr_std = sr.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
combined.attrs['crs'] = sr.attrs['crs']
print(combined)
write_dataset_to_netcdf(combined, sr_out_dc_dask)
time_end = time.time()
timing.append(time_end - time_begin)

# summary
for id, t in enumerate(timing):
    print('Test %d completed in %.1f seconds' % (id, t))
