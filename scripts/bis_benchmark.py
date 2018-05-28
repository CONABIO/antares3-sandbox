import datacube
from madmex.segmentation.bis import Segmentation
import fiona
import os
import itertools
import distributed

dc = datacube.Datacube()
geoarray = dc.load(product = 's2_001_jalisco_2017_0',
                   x=(-103.7, -103.3),
                   y=(20.2, 20.6),
                   measurements=['red_mean', 'green_mean', 'nir_mean', 'swir1_mean',
                                 'swir2_mean', 'ndvi_mean', 'ndmi_mean'])
print(geoarray)

t_list = [30, 40]
s_list = [0.3, 0.5, 0.7, 0.9]
c_list = [0.2, 0.5, 0.7, 0.9]

iterable = list(itertools.product(t_list, s_list, c_list))
print(iterable)

def run_segmentation(x, geoarray):
    t, s, c = x
    out_file = os.path.join('/home/madmex_user/datacube_ingest/tmp/bis_tests',
                            'bis_sentinel_t%d_s%.2f_c%.2f.shp' % (t, s, c))


    seg = Segmentation.from_geoarray(geoarray, t=t, s=s, c=c)
    seg.segment()
    seg.polygonize(crs_out=None)

    # Write to shapefile
    schema = {'geometry': 'Polygon',
              'properties': [('id', 'int')]}

    with fiona.open(out_file, 'w',
                    schema=schema,
                    driver='ESRI Shapefile',
                    crs=seg.crs) as dst:
        for feature in seg.fc:
            dst.write(feature)
    return True

if __name__ == "__main__":
    cluster = distributed.Client()
    c = cluster.map(run_segmentation, iterable,
                    **{'geoarray': geoarray})
    result = cluster.gather(c)
    print(c)
