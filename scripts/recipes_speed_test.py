import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt

arr = np.random.randint(0, 10000, size=(20, 1000, 1000), dtype=np.int16)
date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(1, 320, 16)]
xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list})
sr = xr.Dataset({'blue': xarr, 'green': xarr, 'red': xarr, 'nir': xarr * 2,
                      'swir1': xarr, 'swir2': xarr})
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
sr['ndvi'] = sr.ndvi.astype(np.int16)
print(sr)
sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
print(sr_mean)
sr_min = sr.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
print(sr_min)
sr_max = sr.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
print(sr_max)
sr_std = sr.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
print(sr_std)
# Merge dataarrays
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
print(combined)


