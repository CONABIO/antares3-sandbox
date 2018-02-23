import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
import os
import datacube
from datacube.storage.storage import write_dataset_to_netcdf
from datacube.storage import masking

import dask
import dask.multiprocessing
from dask.diagnostics import ProgressBar

if os.path.isfile('/tmp/sr_reduced.nc'):
    os.remove('/tmp/sr_reduced.nc')

dc = datacube.Datacube(app = 'recipe_madmex_001')
# Load Landsat sr
sr_dask_0 = dc.load(product='ls8_espa_mexico', x=(-104, -102), y=(20, 22),
                  time=(datetime(2017,1,1), datetime(2017, 12, 31)),
                  group_by='solar_day')# dask_chunks={'x': 2000, 'y': 2000})
sr_dask = sr_dask_0.drop('pixel_qa')
sr_dask['ndvi'] = ((sr_dask.nir - sr_dask.red) / (sr_dask.nir + sr_dask.red)) * 10000
sr_dask['ndvi'] = sr_dask.ndvi.astype(np.int16)
sr_mean = sr_dask.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
sr_min = sr_dask.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
sr_max = sr_dask.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
sr_std = sr_dask.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
# Merge dataarrays
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
combined.attrs['crs'] = sr_dask_0.attrs['crs']
print(combined)
# with ProgressBar():
write_dataset_to_netcdf(combined, '/tmp/sr_reduced.nc')


