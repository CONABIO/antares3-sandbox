from rasterio.features import rasterize
from madmex.io.vector_db import VectorDb
from rasterio.features import rasterize
import datacube
from datacube.api import GridWorkflow
from pprint import pprint
from datetime import datetime
from affine import Affine

# Load a test dataset
dc = datacube.Datacube()
gw = GridWorkflow(dc.index , product='ls8_espa_mexico')
tile_dict = gw.list_cells(product='ls8_espa_mexico',
                          x=(-104, -102),
                          y=(19, 21),
                          time=(datetime(2017, 1, 1), datetime(2017, 2, 1)))
tile_list = list(tile_dict.items())
sr = gw.load(tile_list[3][1])

# Visualize Dataset metadata
print(sr)

# Load training data corresponding to that dataset
db = VectorDb()
fc = db.load_training_from_dataset(sr)

# Visualize first element of feature collection
pprint(fc[0])

# Rasterize the feature collection
geom_list = [x['geometry'] for x in fc]
iterable = zip(geom_list, range(1, len(fc) + 1))
aff = Affine(*list(sr.affine)[0:6])
fc_raster = rasterize(iterable, transform=aff, out_shape=(sr.sizes['y'], sr.sizes['x']))
print(fc_raster)
