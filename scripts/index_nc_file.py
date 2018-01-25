from datacube.index._datasets import ProductResource, MetadataTypeResource, DatasetResource
from datacube.index.postgres._connections import PostgresDb
from datacube.model import Dataset

# dict of product
product_def_dict = {'name': 'recipe_1_intermediate_2017',
                    'description': 'Intermediary dataset used for model training and prediction',
                    'metadata_type': 'eo',
                    'metadata': {'platform': {'code': 'multi'},
                                 'instrument': {'name': 'multi'},
                                 'product_type': 'intermediary',
                                 'format': {'name': 'netCDF'}},
                    'storage': {'crs': 'PROJCS["unnamed",GEOGCS["WGS 84",DATUM["unknown",SPHEROID["WGS84",6378137,6556752.3141]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",17.5],PARAMETER["standard_parallel_2",29.5],PARAMETER["latitude_of_origin",12],PARAMETER["central_meridian",-102],PARAMETER["false_easting",2500000],PARAMETER["false_northing",0]]',
                                 'resolution': {'x': 30,
                                                'y': -30}},
                    'measurements': [{'name': 'blue',
                                      'units': 'reflectance',
                                      'dtype': 'float64',
                                      'nodata': -9999},
                                     {'name': 'green',
                                      'units': 'reflectance',
                                      'dtype': 'float64',
                                      'nodata': -9999},
                                     {'name': 'red',
                                      'units': 'reflectance',
                                      'dtype': 'float64',
                                      'nodata': -9999},
                                     {'name': 'nir',
                                      'units': 'reflectance',
                                      'dtype': 'float64',
                                      'nodata': -9999},
                                     {'name': 'swir1',
                                      'units': 'reflectance',
                                      'dtype': 'float64',
                                      'nodata': -9999},
                                     {'name': 'swir2',
                                      'units': 'reflectance',
                                      'dtype': 'float64',
                                      'nodata': -9999},
                                     {'name': 'elevation',
                                      'units': 'meter',
                                      'dtype': 'int16',
                                      'nodata': -32768},
                                     {'name': 'slope',
                                      'units': 'degree',
                                      'dtype': 'float32',
                                      'nodata': -9999},
                                     {'name': 'aspect',
                                      'units': 'degree',
                                      'dtype': 'float32',
                                      'nodata': -9999}]}

# Product add
db = PostgresDb.from_config()
meta_resource = MetadataTypeResource(db)
product_resource = ProductResource(db, meta_resource)
dataset_type = product_resource.add_document(product_def_dict)
print(product_resource)
print(dataset_type)

# Prepare metadata

# Dataset add
dataset_resource = DatasetResource(db, product_resource)
dataset = Dataset()
print(dataset_resource)

