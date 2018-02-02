import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt

arr = np.random.randint(0, 10000, size=(20, 1000, 1000), dtype=np.int16)
date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(20)]
xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list})
xset = xr.Dataset({'blue': xarr, 'green': xarr, 'red': xarr})
print(xset)
xset_mean = xset.mean('time', keep_attrs=True, dtype=np.int16)
print(xset_mean)

# Pure numpy
arr_mean = arr.mean(axis=0, dtype=np.int16)
print(arr_mean.dtype)
