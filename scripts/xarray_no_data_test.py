import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
from xarray.testing import assert_identical

def to_float(x):
    x_float = x.where(x != x.attrs['nodata'])
    return x_float

def to_int(x):
    x[np.isnan(x)] = x.attrs['nodata']
    return x.astype('int16')

# Build test data
arr = np.array([1,2,-9999], dtype=np.int16)
date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(3)]
xarr = xr.DataArray(arr, dims=['time'], coords={'time': date_list},
                    attrs={'nodata': -9999})
xset = xr.Dataset({'blue': xarr, 'green': xarr, 'red': xarr})
print(xset)

# Round trip int to float (with nodata replaced by nan) to int
xset_float = xset.apply(func=to_float, keep_attrs=True)
print(xset_float)
xset_int = xset_float.apply(to_int, keep_attrs=True)
print(xset_int)
# assert_identical(xset, xset_int)

xset['red'].attrs['nodata'] = 23
print(xset['red'].attrs)
