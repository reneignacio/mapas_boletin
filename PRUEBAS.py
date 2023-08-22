# -*- coding: utf-8 -*-
import arcpy
import os

regiones = {
    "R01": "Región de Tarapacá",
    "R02": "Región de Antofagasta",
    "R03": "Región de Atacama",
    "R04": "Región de Coquimbo",
    "R05": "Región de Valparaíso",
    "R06": "Región del Libertador Gral. Bernardo O'Higgins",
    "R07": "Región del Maule",
    "R08": "Región de Bío-Bío",
    "R09": "Región de La Araucanía",
    "R10": "Región de Los Lagos",
    "R11": "Región de Aysén del Gral. Carlos Ibañez del Campo",
    "R12": "Región de Magallanes y la Antártica Chilena",
    "R13": "Región de Metropolitana de Santiago",
    "R14": "Región de Los Ríos",
    "R15": "Región de Arica y Parinacota",
    "R16": "Región del Ñuble"
}

mxd = arcpy.mapping.MapDocument("C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\ANOMALIA_SAVI2.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layers = arcpy.mapping.ListLayers(mxd)

for layer in layers:
    if layer.isRasterLayer:
        arcpy.mapping.RemoveLayer(df, layer)
        print("{} removida".format(layer.name))

# Cargar capa SAVI.tif
for region in regiones.keys():
    R = region
    ruta_anomalia_SAVI_tif = "C:\\Users\\INIA\\Desktop\\2023-06-26_v2\\{0}\\TIF\\ANOMALIA\\{0}_Anomalia_SAVI_median_ZA.tif".format(R)
    if os.path.exists(ruta_anomalia_SAVI_tif):
        try:
            capa_anomalia = arcpy.mapping.Layer(ruta_anomalia_SAVI_tif)
            arcpy.mapping.AddLayer(df, capa_anomalia, "BOTTOM")
            print("tif {} añadido".format(R))
        except Exception as e:
            print("Error cargando capa para la region {}: {}".format(R, e))

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mxd.save()
# Extraer solo los nombres y ordenar la lista alfabéticamente
layer_names = sorted([layer.name for layer in arcpy.mapping.ListLayers(mxd)])

# Filtrar y almacenar los nombres de las capas que contienen "Anomalia_SAVI"
anomalia_savi_layers = [name for name in layer_names if "Anomalia_SAVI" in name]

# Contar y mostrar los nombres de las capas
anomalia_savi_count = len(anomalia_savi_layers)
print(anomalia_savi_count)
print(anomalia_savi_layers)

# esto ahora hay que añadirlo a ANOMALIA_SAVI.py, falta agregar comunas y region y luego copiar el estilo de un archivo
