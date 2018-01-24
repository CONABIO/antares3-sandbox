import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
import gc

arr = np.random.rand(20, 5000, 5000)
date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(20)]
xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list})
xarr.to_netcdf('/tmp/xarray_dask_test_in.nc')
# Clean variables and memory
arr = None
xarr = None
gc.collect()

xarr_nc = xr.open_dataset('/tmp/xarray_dask_test_in.nc', chunks = {'x': 500, 'y': 500})
xarr_nc_mean = xarr_nc.mean('time')
xarr_nc_mean.to_netcdf('/tmp/xarray_dask_test_out.nc')


