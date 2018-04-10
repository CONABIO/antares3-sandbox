import xarray as xr
import numpy as np
from datetime import datetime
import datetime as dt
import time
import bottleneck


arr = np.random.randint(0, 1000, size=(10, 200, 200), dtype=np.int16)
arr = np.where(arr > 800, np.nan, arr)
date_list = [datetime(2018, 1, 1) + dt.timedelta(delta) for delta in range(10)]
xarr = xr.DataArray(arr, dims=['time', 'x', 'y'], coords={'time': date_list})
sr = xr.Dataset({'blue': xarr,
                 'green': xarr,
                 'red': xarr * 2})
print(sr)

begin = time.time()
sr_20 = sr.quantile([0.2], dim='time')
end = time.time()
print('xr quantile execution in %.2f seconds' % (end - begin))

# Dask
sr_ds = sr.chunk({'x': 100, 'y': 100})
print(sr_ds)

begin = time.time()
sr_ds_20 = sr.quantile([0.2], dim='time').compute()
end = time.time()
print('dask quantile execution in %.2f seconds' % (end - begin))

# Assert equal
xr.testing.assert_allclose(sr_20, sr_ds_20)

