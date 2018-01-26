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
             time=(datetime(2017, 6, 1), datetime(2018, 1, 1)), group_by='solar_day',
             dask_chunks={'x': 2000, 'y': 2000})
sr['ndvi'] = (sr.nir - sr.red) / (sr.nir + sr.red)
terrain = dc.load(product='srtm_cgiar_mexico', like=sr, time=(datetime(1970, 1, 1), datetime(2018, 1, 1)),
                  dask_chunks={'x': 2000, 'y': 2000})
clear = masking.make_mask(sr.pixel_qa, clear=True)
sr_clear = sr.where(clear)
sr_clear2 = sr_clear.drop('pixel_qa')
sr_mean = sr_clear2.mean('time', keep_attrs=True)
sr_mean.rename({'blue': 'blue_mean',
                'green': 'green_mean',
                'red': 'red_mean',
                'nir': 'nir_mean',
                'swir1': 'swir1_mean',
                'swir2': 'swir2_mean',
                'ndvi': 'ndvi_mean'}, inplace=True)
sr_min = sr_clear2.min('time', keep_attrs=True)
sr_min.rename({'blue': 'blue_min',
                'green': 'green_min',
                'red': 'red_min',
                'nir': 'nir_min',
                'swir1': 'swir1_min',
                'swir2': 'swir2_min',
                'ndvi': 'ndvi_min'}, inplace=True)
sr_max = sr_clear2.max('time', keep_attrs=True)
sr_max.rename({'blue': 'blue_max',
                'green': 'green_max',
                'red': 'red_max',
                'nir': 'nir_max',
                'swir1': 'swir1_max',
                'swir2': 'swir2_max',
                'ndvi': 'ndvi_max'}, inplace=True)
sr_std = sr_clear2.std('time', keep_attrs=True)
sr_std.rename({'blue': 'blue_std',
                'green': 'green_std',
                'red': 'red_std',
                'nir': 'nir_std',
                'swir1': 'swir1_std',
                'swir2': 'swir2_std',
                'ndvi': 'ndvi_std'}, inplace=True)
combined = xr.merge([sr_mean, sr_min, sr_max, sr_std, terrain])
combined.attrs['crs'] = sr.attrs['crs']
print(combined)
with ProgressBar():
    write_dataset_to_netcdf(combined, nc_file)
