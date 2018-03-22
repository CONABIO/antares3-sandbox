from madmex.segmentation.slic import Segmentation
from madmex.wrappers import gwf_query
from madmex.util.xarray import to_float
from datacube.storage import masking
from madmex.models import SegmentationInformation
from pprint import pprint

gwf, tiles_list = gwf_query(product='ls8_espa_mexico', region='Jalisco',
                            begin = '2017-01-01', end='2017-03-31')
geoarray = gwf.load(list(tiles_list)[5][1])
clear = masking.make_mask(geoarray.pixel_qa, clear=True)
geoarray = geoarray.where(clear)
geoarray = geoarray.drop('pixel_qa')
geoarray = geoarray.apply(func=to_float, keep_attrs=True)
geoarray = geoarray.mean('time', keep_attrs=True, skipna=True)
print(geoarray)

meta = SegmentationInformation(algorithm='slic', datasource='landsat8',
                               parameters="{'compactness': 0.1}",
                               datasource_year='January 2017')
try:
    meta.save()
except Exception as e:
    pass


seg = Segmentation.from_geoarray(geoarray, n_segments=1000000, compactness=1)
seg.segment()
seg.polygonize()
seg.to_db(meta)

print(seg.fc[1])
