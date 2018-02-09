from datacube.index.postgres._connections import PostgresDb
from datacube.index._api import Index
from datacube.api import GridWorkflow
from pprint import pprint
import numpy

db = PostgresDb.from_config()
i = Index(db)
gwf = GridWorkflow(i, product='ls8_espa_mexico')
tile_list = gwf.list_tiles(product='ls8_espa_mexico')
print(gwf.load(tile_list[(16, -13, numpy.datetime64('2017-12-07T17:11:43.222701000'))]))
