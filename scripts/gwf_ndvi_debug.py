from datacube.api import GridWorkflow
import datacube
from datetime import datetime
import os
import datacube
from datacube.storage.storage import write_dataset_to_netcdf
from datacube.storage import masking
import xarray as xr
import numpy as np
import dask

from madmex.util.xarray import to_int

dask.set_options(get=dask.get)

from datetime import datetime
import logging
logger = logging.getLogger(__name__)

def run(tile, gwf, center_dt):
    """Basic datapreparation recipe 001

    Computes mean NDVI for a landsat collection over a given time frame

    Args:
        tile (tuple): Tuple of (tile indices, Tile object). Tile object can be
            loaded as xarray.Dataset using gwf.load()
        gwf (GridWorkflow): GridWorkflow object instantiated with the corresponding
            product
        center_dt (datetime): Date to be used in making the filename

    Return:
        str: The filename of the netcdf file created
    """
    try:
        center_dt = center_dt.strftime("%Y-%m-%d")
        # TODO: Need a more dynamic way to handle this filename (e.g.: global variable for the path up to datacube_ingest)
        nc_filename = os.path.expanduser('~/datacube_ingest/recipes/landsat_8_ndvi_mean/ndvi_mean_%d_%d_%s.nc' % (tile[0][0], tile[0][1], center_dt))
        if os.path.isfile(nc_filename):
            raise ValueError('%s already exist' % nc_filename)
        # Load Landsat sr
        sr = gwf.load(tile[1],
                      dask_chunks={'x': 1667, 'y': 1667},
                     )
        # Compute ndvi
        sr['ndvi'] = (sr.nir - sr.red) / (sr.nir + sr.red) * 10000
        clear = masking.make_mask(sr.pixel_qa, clear=True)
        ndvi = sr.drop(['pixel_qa', 'blue', 'red', 'green', 'nir', 'swir1', 'swir2'])
        ndvi_clear = ndvi.where(clear)
        # Run temporal reductions and rename DataArrays
        ndvi_mean = ndvi_clear.mean('time', keep_attrs=True)
        ndvi_mean['ndvi'].attrs['nodata'] = -9999
        ndvi_mean_int = ndvi_mean.apply(to_int)
        ndvi_mean_int.attrs['crs'] = sr.attrs['crs']
        write_dataset_to_netcdf(ndvi_mean_int, nc_filename,
                                netcdfparams={'zlib': True})
        return nc_filename
    except Exception as e:
        print('Tile (%d, %d) not processed. %s' % (tile[0][0], tile[0][1], e))
        raise
        return None


product = 'ls8_espa_mexico'
begin = datetime(2017, 1, 1)
end = datetime(2017, 3, 1)
long = (-106, -102)
lat = (19, 23)
center_dt = datetime(2017, 2, 1)

# GridWorkflow object
dc = datacube.Datacube()
gwf = GridWorkflow(dc.index, product=product)
tile_dict = gwf.list_cells(product=product, time=(begin, end),
                           x=long, y=lat)
# Iterable (dictionary view (analog to list of tuples))
iterable = list(tile_dict.items())
run(iterable[0], gwf=gwf, center_dt=center_dt)
