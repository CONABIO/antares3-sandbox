import numpy as np
import sys
import json
import os

from shutil import copyfile
from scipy.constants.constants import hectare
from osgeo import gdal, osr

#rmartinez

def open_tiff(path):
    '''
        Given a raster path, it opens it and returns the dataset.
    '''
    print('Reading raster path: %s'  % (path) )
    return gdal.Open(path)

def get_NoData(dataset):
    '''
        Given a dataset, it returns the raster's NoData value
    '''
    return dataset.GetRasterBand(1).GetNoDataValue()

def get_resolution(dataset):
    '''
        Given a dataset, it returns the x and y resolution
    '''
    geotransform = dataset.GetGeoTransform()
    x_resolution = geotransform[1]
    y_resolution = geotransform[5]
    return x_resolution, y_resolution

def get_pixel_area(x, y):
    '''
        Given the x and y resolutions, it returns the pixel's area
    '''
    return abs(x * y)

def get_natural_raster_block(dataset):
    '''
        Given a dataset, it returns the "natural" block size
        and the total XY size
    '''
    block_sizes = dataset.GetRasterBand(1).GetBlockSize()
    x_block_size = block_sizes[0]
    y_block_size = block_sizes[1]
    xsize = dataset.GetRasterBand(1).XSize
    ysize = dataset.GetRasterBand(1).YSize
    return x_block_size, y_block_size, xsize, ysize

def area_per_block(class_pixels, pixel_resolution):
    '''
        This method returns the area of the given pixels per hectare
    '''
    return  (pixel_resolution * class_pixels) / hectare

def read_by_block(dataset, nodata, pixel_area, x_block_size, y_block_size, xsize, ysize):
    '''
        This method reads the raster by blocks and returns a dictionary with
        all classes as keys and their area values found in it.
    '''
    blocks = 0
    general_dict = dict ()
    for y in range(0, ysize, y_block_size):
        partial_area = []
        partial_classes = []
        if y + y_block_size < ysize:
            rows = y_block_size
        else:
            rows = ysize - y
        for x in range(0, xsize, x_block_size):
            if x + x_block_size < xsize:
                cols = x_block_size
            else:
                cols = xsize - x
            array = dataset.GetRasterBand(1).ReadAsArray(x, y, cols, rows)
            # Getting id's of distinct classes in the current block
            arr_class_info = np.unique(array, return_counts=True)
            for i in range(len(arr_class_info[0])):
                class_id = arr_class_info[0][i]
                if class_id != nodata:
                    num_pixels_per_class = arr_class_info[1][i]
                    area_per_class = area_per_block(num_pixels_per_class,pixel_area)
                    #logger.info('Class ID: %s \t Area in this class:  %s \t [ha] '  % (class_id, area_per_class))
                    partial_area.append(area_per_class)
                    partial_classes.append(str(class_id))
                    # Adding new area values to the same class key
                    general_dict.setdefault(str(class_id), []).append(area_per_class)
            print('Proccessing block %s: \t %s distinct class(es) found in this block. \t %s hectare(s) in this block.' %(y,len(partial_classes),sum(partial_area)))
            del array
            blocks += 1
    return general_dict

rasterfile   = sys.argv[1]
schema       = sys.argv[2]
templete_pie = sys.argv[3]
templete_bar = sys.argv[4]

dest_pie = os.getcwd() + "/"
dest_bar = os.getcwd() + "/"

copyfile(templete_pie, dest_pie+os.path.basename(rasterfile).split('.')[0]+'_pie.json')
copyfile(templete_bar, dest_bar+os.path.basename(rasterfile).split('.')[0]+'_bar.json')

# -------- Edita titulo en json de barra --------
with open(dest_bar+os.path.basename(rasterfile).split('.')[0]+'_bar.json', 'r') as barra:
    barra_arr = json.load(barra)

print(barra_arr[0]["name"])
barra_arr[0]["name"] = os.path.basename(rasterfile).split('.')[0].replace("_", " ") + " clases de cobertura."

with open(dest_bar+os.path.basename(rasterfile).split('.')[0]+'_bar.json', 'w') as barra:
    json.dump(barra_arr, barra, indent=2)
#-----------------------------------------------

ds = open_tiff(rasterfile)
x, y = get_resolution(ds)
print('Raster resolution: x = %s , y = %s'  % (x, y))
pixel_area = get_pixel_area(x, y)
print('Pixel area: %s'  % (pixel_area))
nodata = get_NoData(ds)
print('No-Data value: %s'  % (nodata))
x_block, y_block, xsize, ysize = get_natural_raster_block(ds)
print('Getting block size')
dict = read_by_block(ds, nodata, pixel_area, x_block, y_block, xsize, ysize)

del ds

raster_keys = list(dict.keys())

with open(schema, 'r') as sfile:
    array = json.load(sfile)

list_class_in_raster = []
id_class_in_raster = []
for i in raster_keys:
    list_class_in_raster.append(array[str(i)]["classname"])
    id_class_in_raster.append(array[str(i)]["id"])

with open(templete_pie, 'r') as jfile:
    j_array = json.load(jfile)

for i in range(len(list_class_in_raster)):
    for clase in j_array[0]["data"]:
        if list_class_in_raster[i] == clase["name"]:
            print(list_class_in_raster[i], raster_keys[i], id_class_in_raster[i], sum(dict[raster_keys[i]]))

            # ------ Agrega hectareas en json de pie segun la clase  --------
            with open(dest_pie+os.path.basename(rasterfile).split('.')[0]+'_pie.json', 'r') as pie:
                pie_arr = json.load(pie)

            pie_arr[0]["data"][id_class_in_raster[i]]["y"] = float('%.3f'%(sum(dict[raster_keys[i]])))

            with open(dest_pie+os.path.basename(rasterfile).split('.')[0]+'_pie.json', 'w') as pie:
                json.dump(pie_arr, pie, indent=2)
            # ----------------------------------------------------------------

            # ------ Agrega hectareas en json de barra segun la clase  --------
            with open(dest_bar+os.path.basename(rasterfile).split('.')[0]+'_bar.json', 'r') as barra:
                bar_arr = json.load(barra)

            bar_arr[0]["data"][id_class_in_raster[i]][1] = float('%.3f'%(sum(dict[raster_keys[i]])))

            with open(dest_bar+os.path.basename(rasterfile).split('.')[0]+'_bar.json', 'w') as barra:
                json.dump(bar_arr, barra, indent=2)
            # ----------------------------------------------------------------
print ("############################################")
