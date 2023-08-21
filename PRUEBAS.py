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
savi=0
import arcpy
import os
mxd = arcpy.mapping.MapDocument("C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\ANOMALIA_SAVI.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layers = arcpy.mapping.ListLayers(mxd)[0]

#modificion





#Cargar capa SAVI.tif
for region in regiones.keys():
    R=region
    ruta_anomalia_SAVI_tif="C:\\Users\\INIA\\Desktop\\2023-06-26_v2\\{0}\\TIF\\ANOMALIA\\{0}_Anomalia_SAVI_median_ZA.tif".format(R)
    if os.path.exists(ruta_anomalia_SAVI_tif):
        capa_anomalia=arcpy.mapping.Layer(ruta_anomalia_SAVI_tif)
        arcpy.mapping.AddLayer(df,capa_anomalia,"BOTTOM")
        print("tif region {} añadido".format(R))
        savi=savi+1        
if savi==3:
    print("se subieron {} capas de SAVI, esta correcto".format(savi))
else: 
    print("el numero de capas SAVI subidas es {} y deberian ser 3".format(savi))

#Cargar shp comunas.tif
for region in regiones.keys():
    R=region
    ruta_anomalia_SAVI_tif="C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\shape\\comunas\\{}.shp".format(R)
    if os.path.exists(ruta_anomalia_SAVI_tif):
        capa_anomalia=arcpy.mapping.Layer(ruta_anomalia_SAVI_tif)
        arcpy.mapping.AddLayer(df,capa_anomalia,"BOTTOM")
        print("tif region {} añadido".format(R))
        savi=savi+1        
if savi==3:
    print("se subieron {} capas de SAVI, esta correcto".format(savi))
else: 
    print("el numero de capas SAVI subidas es {} y deberian ser 3".format(savi))

#MEJOR CAMBIARLO POR ALGO ASI, QUE REVISA LAS CAPAS DENTRO DEL MXD

# Extraer solo los nombres y ordenar la lista alfabéticamente
layer_names = sorted([layer.name for layer in layers])
# Filtrar y contar los nombres de las capas que contienen "Anomalia_SAVI"
anomalia_savi_count = len([name for name in layer_names if "Anomalia_SAVI" in name])
print(anomalia_savi_count)










"""
R="R02"
ruta_anomalia_SAVI_tif="C:\\Users\\INIA\\Desktop\\2023-06-26_v2\\{0}\\TIF\\ANOMALIA\\{0}_Anomalia_SAVI_median_ZA.tif".format(R)
capa_anomalia=arcpy.mapping.Layer(ruta_anomalia_SAVI_tif)
arcpy.mapping.AddLayer(df,capa_anomalia)"""