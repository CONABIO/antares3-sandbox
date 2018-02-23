import netCDF4 as nc
import xarray as xr

# with nc.MFDataset('/home/madmex_user/datacube_ingest/LS8_espa/mexico/*.nc') as src:
    # print(src)
sr = xr.open_mfdataset('/home/madmex_user/datacube_ingest/LS8_espa/mexico/LS8_espa_11_-12*.nc',
                       chunks={'x': 1000, 'y': 1000})
sr['ndvi'] = ((sr.nir - sr.red) / (sr.nir + sr.red)) * 10000
# sr_mean = sr.mean('time', keep_attrs=True, dtype=np.int16, skipna=True)
# sr_mean.rename({'blue': 'blue_mean',
                # 'green': 'green_mean',
                # 'red': 'red_mean',
                # 'nir': 'nir_mean',
                # 'swir1': 'swir1_mean',
                # 'swir2': 'swir2_mean',
                # 'ndvi': 'ndvi_mean'}, inplace=True)
# sr_min = sr.min('time', keep_attrs=True, dtype=np.int16, skipna=True)
# sr_min.rename({'blue': 'blue_min',
                # 'green': 'green_min',
                # 'red': 'red_min',
                # 'nir': 'nir_min',
                # 'swir1': 'swir1_min',
                # 'swir2': 'swir2_min',
                # 'ndvi': 'ndvi_min'}, inplace=True)
# sr_max = sr.max('time', keep_attrs=True, dtype=np.int16, skipna=True)
# sr_max.rename({'blue': 'blue_max',
                # 'green': 'green_max',
                # 'red': 'red_max',
                # 'nir': 'nir_max',
                # 'swir1': 'swir1_max',
                # 'swir2': 'swir2_max',
                # 'ndvi': 'ndvi_max'}, inplace=True)
# sr_std = sr.std('time', keep_attrs=True, dtype=np.int16, skipna=True)
# sr_std.rename({'blue': 'blue_std',
                # 'green': 'green_std',
                # 'red': 'red_std',
                # 'nir': 'nir_std',
                # 'swir1': 'swir1_std',
                # 'swir2': 'swir2_std',
                # 'ndvi': 'ndvi_std'}, inplace=True)
# combined = xr.merge([sr_mean, sr_min, sr_max, sr_std])
# combined.attrs['crs'] = sr.attrs['crs']
# print(combined)
# write_dataset_to_netcdf(combined, sr_out_dc_dask)
# time_end = time.time()
# timing.append(time_end - time_begin)
print(sr)# 
sr.to_netcdf('/tmp/mfread_test.nc')
