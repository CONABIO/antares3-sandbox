Para generar un json dado un raster de cobertura de suelo, se debe seguir la siguiente sintaxsis 

```python
python generate_json.py /path/to/raster.tif /path/to/schema_cobertura<08,17,31>.json /path/to/templete_cobertura<08,17,31>_pie.json /path/to/templete_cobertura<08,17,31>_bar.json
```

El primer archivo es el raster del cual se pretende generar un json con las hectáreas por clase dado un esquema de clasificación especiífico. El archivo de schema contiene el esquema de clasificación del raster, esta puede ser de 8, 17 o 31 clases. Los siguietes dos archivos son respectivamente los templates json de para gráficas de pie y de barras.
El resultado son dos json con el nombre del raster y que se crean en el directorio o nivel donde se ejecuta el comando, un archivo es un json para gráficas de pie y otro para gráficas de barras.
Es importante mencionar que tanto el archivo de esquema como los dos templates tienen, en el mismo orden, las clases que espera leer del raster. Si el orden de las clases fuera distinto entre los tres archivos o almenos uno de ellos, el análisis no resulta de utilidad pues asignaría hectáreas a clases que no le corresponden. 
