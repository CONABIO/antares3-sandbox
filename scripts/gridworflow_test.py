import os
from datacube.index.postgres._connections import PostgresDb
from datacube.index._api import Index
from datacube.api import GridWorkflow
from datacube.storage.storage import write_dataset_to_netcdf
from pprint import pprint
import numpy

nc_filename = os.path.expanduser('~/datacube_ingest/recipes/ndvi_mean/ndvi_mean_%d_%d_%s.nc' % (12, -16, '1987'))

db = PostgresDb.from_config()
i = Index(db)
gwf = GridWorkflow(i, product='ls8_espa_mexico')
cells_list = gwf.list_cells(product='ls8_espa_mexico', x=(-106, -101), y=(19,23))
sr = gwf.load(cells_list[(12, -16)],
              dask_chunks={'x': 1000, 'y': 1000})
sr['ndvi'] = (sr.nir - sr.red) / (sr.nir + sr.red) * 10000
ndvi = sr.drop(['pixel_qa', 'blue', 'red', 'green', 'nir', 'swir1', 'swir2'])
# Run temporal reductions and rename DataArrays
ndvi_mean = ndvi.mean('time', keep_attrs=True)
ndvi_mean = ndvi_mean.astype('int16')
ndvi_mean.attrs['crs'] = sr.attrs['crs']
write_dataset_to_netcdf(ndvi_mean, nc_filename)
print(nc_filename)
