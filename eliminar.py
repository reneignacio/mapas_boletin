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
mxd = arcpy.mapping.MapDocument("C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\vacio.mxd")
# Establecer la geodatabase como el espacio de trabajo
arcpy.env.workspace = r"C:\Users\INIA\Desktop\MAPA_ANOMALIA_PYTHON\Geodatabase.gdb"
df = arcpy.mapping.ListDataFrames(mxd)[0]
layers = arcpy.mapping.ListLayers(mxd)

for layer in layers:
    if layer.isRasterLayer and layer.name != "LEYENDA_v2.tif":
        arcpy.mapping.RemoveLayer(df, layer)
        print("{} removida".format(layer.name))


# Cargar capa SAVI.tif
for region in regiones.keys():
    R = region
    ruta_anomalia_SAVI_tif = "C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\data\\{0}\\TIF\\ANOMALIA\\{0}_Anomalia_SAVI_median_ZA.tif".format(R)
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
#SAVI AÑADIDO

 # Añadir la capa leyenda.tif al MXD
ruta_leyenda_tif = "C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\formato\\LEYENDA_v2.tif"
try:
    leyenda_tif_layer = arcpy.mapping.Layer(ruta_leyenda_tif)
    arcpy.mapping.AddLayer(df, leyenda_tif_layer, "TOP")
except Exception as e:
    print("Error cargando la capa LEYENDA_v2.tif: {}".format(e))
    # Detiene la ejecución si hay un error al cargar la capa
    exit()

arcpy.RefreshActiveView()
arcpy.RefreshTOC()

# Aplicar el estilo desde el archivo .lyr a la capa leyenda.tif
leyenda_layer = arcpy.mapping.ListLayers(mxd, "LEYENDA_v2.tif")[0]
leyenda_layer.visible = False
ruta_estilo = "C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\formato\\ANOMALIA\\LEYENDA_TIF.lyr"
try:
    # Usar el método UpdateLayer para aplicar el estilo y asegurarse de que se aplique correctamente
    sourceLayer = arcpy.mapping.Layer(ruta_estilo)
    arcpy.mapping.UpdateLayer(df, leyenda_layer, sourceLayer, True)
except Exception as e:
    print("Error aplicando el estilo a la capa LEYENDA_v2.tif: {}".format(e))
    # Detiene la ejecución si hay un error al aplicar el estilo
    exit()

# Guardar cambios
mxd.save()


""" 
# Añadir la capa leyenda.tif al MXD
ruta_leyenda_tif = r"C:\Users\INIA\Desktop\MAPA_ANOMALIA_PYTHON\formato\LEYENDA_v2.tif"

# Verificar si el archivo existe
if not os.path.exists(ruta_leyenda_tif):
    print("El archivo LEYENDA_v2.tif no existe en la ruta especificada.")
    exit()

try:
    leyenda_tif_layer = arcpy.mapping.Layer(ruta_leyenda_tif)
    arcpy.mapping.AddLayer(df, leyenda_tif_layer, "TOP")
except Exception as e:
    print("Error cargando la capa LEYENDA_v2.tif: {}".format(e))
    # Detiene la ejecución si hay un error al cargar la capa
    exit()

arcpy.RefreshActiveView()
arcpy.RefreshTOC()

# Verificar si la capa LEYENDA_v2.tif se agregó correctamente
leyenda_layers = arcpy.mapping.ListLayers(mxd, "LEYENDA_v2.tif")
if not leyenda_layers:
    print("La capa LEYENDA_v2.tif no se encontró después de ser añadida.")
    exit()

leyenda_layer = leyenda_layers[0]
leyenda_layer.visible = False

ruta_estilo = r"C:\Users\INIA\Desktop\MAPA_ANOMALIA_PYTHON\formato\ANOMALIA\LEYENDA_TIF.lyr"

# Verificar si el archivo de estilo .lyr existe
if not os.path.exists(ruta_estilo):
    print("El archivo de estilo LEYENDA_TIF.lyr no existe en la ruta especificada.")
    exit()

try:
    # Usar el método UpdateLayer para aplicar el estilo y asegurarse de que se aplique correctamente
    sourceLayer = arcpy.mapping.Layer(ruta_estilo)
    arcpy.mapping.UpdateLayer(df, leyenda_layer, sourceLayer, True)
except Exception as e:
    print("Error aplicando el estilo a la capa LEYENDA_v2.tif: {}".format(e))
    # Detiene la ejecución si hay un error al aplicar el estilo
    exit()

# Guardar cambios
mxd.save()






legend.autoAdd = True
leyenda_lyr_path = "C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\formato\\ANOMALIA\\LEYENDA_TIF.lyr"
leyenda_layer_from_lyr = arcpy.mapping.Layer(leyenda_lyr_path)
arcpy.mapping.AddLayer(df, leyenda_layer_from_lyr, "TOP")

# Extraer solo los nombres y ordenar la lista alfabéticamente
layer_names = sorted([layer.name for layer in arcpy.mapping.ListLayers(mxd)])
# Filtrar y almacenar los nombres de las capas que contienen "Anomalia_SAVI"
anomalia_savi_layers = [name for name in layer_names if "LEYENDA" in name]
anomalia_savi_count = len(anomalia_savi_layers)
print(anomalia_savi_count)
print(anomalia_savi_layers) """