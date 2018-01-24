import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt

arr = np.random.rand(10, 10000, 10000)
date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(10)]
xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list}, name = 'loic')
xarr2 = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list}, name = 'cyril')
dataset = xr.merge([xarr, xarr2])
print(dataset)

dataset.to_netcdf('/LUSTRE/MADMEX/write_speed_test.nc')

