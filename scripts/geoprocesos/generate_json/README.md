Para generar un json dado un raster de cobertura de suelo, se debe seguir la siguiente sintaxsis 

```python
python generate_json.py /path/to/raster.tif /path/to/schema_cobertura<08,17,31>.json /path/to/templete_cobertura<08,17,31>_pie.json /path/to/templete_cobertura<08,17,31>_bar.json
```

El primer archivo es el raster del cual se pretende generar un json con las hectáreas por clase dado un esquema de clasificación especiífico. El archivo de schema contiene el esquema de clasificación del raster, esta puede ser de 8, 17 o 31 clases. Los siguietes dos archivos son respectivamente los templates json de para gráficas de pie y de barras.
El resultado es un json con el nombre del raster y que se crea en el directorio o nivel donde se encuentra el archivo generate_json.py
