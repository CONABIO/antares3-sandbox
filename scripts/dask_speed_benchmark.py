import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
import gc

import dask
import dask.multiprocessing
from dask.diagnostics import ProgressBar
# dask.set_options(get=dask.get)

# arr = np.random.randint(0, 10000, size=(20, 10000, 10000), dtype=np.int16)
# date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(20)]
# xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list})
# sr = xr.Dataset({'blue': xarr, 'green': xarr, 'red': xarr, 'nir': xarr * 2,
                      # 'swir1': xarr, 'swir2': xarr})
# sr.to_netcdf('/tmp/sr_ts.nc')
# sr = None
# xarr = None
# gc.collect()

sr_dask = xr.open_dataset('/tmp/sr_ts.nc',)
                          # chunks={'x': 2000, 'y': 2000})
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
print(combined)
# with ProgressBar():
combined.to_netcdf('/tmp/sr_reduced.nc')

