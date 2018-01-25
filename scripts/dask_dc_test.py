import datacube
from datacube.storage.storage import write_dataset_to_netcdf
from datacube.storage import masking
import os
import xarray as xr
from datetime import datetime
from pprint import pprint

import dask
import dask.multiprocessing
from dask.diagnostics import ProgressBar
dask.set_options(get=dask.multiprocessing.get)

nc_file = '/tmp/datacube_dask_test.nc'

try:
    os.remove(nc_file)
except Exception:
    pass

dc = datacube.Datacube(app = 'dask_test')
sr = dc.load(product='ls8_espa_mexico', x=(-103, -102), y=(22, 21),
             time=(datetime(2017, 1, 1), datetime(2018, 1, 1)), group_by='solar_day',
             dask_chunks={'x': 2000, 'y': 2000})
terrain = dc.load(product='srtm_cgiar_mexico', like=sr, time=(datetime(1970, 1, 1), datetime(2018, 1, 1)),
                  dask_chunks={'x': 2000, 'y': 2000})
clear = masking.make_mask(sr.pixel_qa, clear=True)
sr_clear = sr.where(clear)
sr_clear2 = sr_clear.drop('pixel_qa')
sr_mean = sr_clear2.mean('time')
combined = xr.merge([sr_mean, terrain])
combined.attrs['crs'] = sr.attrs['crs']
with ProgressBar():
    write_dataset_to_netcdf(combined, nc_file)
