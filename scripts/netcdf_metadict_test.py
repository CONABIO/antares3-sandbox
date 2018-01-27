from madmex.indexing import metadict_from_netcdf
import yaml

from pprint import pprint
from datetime import datetime

nc_file = '/LUSTRE/MADMEX/tasks/2018_tasks/datacube_madmex/datacube_directories_mapping_docker_2/tmp_antares-3/datacube_dask_test.nc'

with open('/home/ldutrieux/.config/madmex/indexing/landsat_8_espa_scenes.yaml') as src:
    description = yaml.load(src)

pprint(description)

metadict = metadict_from_netcdf(nc_file, description, datetime(2016, 7, 1))
pprint(metadict)
