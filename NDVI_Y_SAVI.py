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

veg_index="NDVI" #SAVI o NDVI
fecha="26 de junio al 11 de julio de 2023"
#os.chdir("D:/mapas_boletin/mapas_boletin")
mxd = arcpy.mapping.MapDocument("ANOMALIA_{}.mxd".format(veg_index))
df = arcpy.mapping.ListDataFrames(mxd)[0]
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
layers = arcpy.mapping.ListLayers(mxd, "", df)

# Palabras clave para buscar y eliminar
keywords = [veg_index, "Lagos_R", "Glaciares_R","Regional"]
for layer in layers:
    for keyword in keywords:
        if keyword in layer.name:
            arcpy.mapping.RemoveLayer(df, layer)
            print("{} removida".format(layer.name))
            break  

#propiedades leyenda
legend.autoAdd = False
legend.elementHeight = 4.73845
legend.elementPositionX = 11.5270
legend.elementPositionY = 3.98255
legend.elementWidth = 2.4576


#CARGAR ARCHIVOS PARA LEYENDA
ruta_leyenda_tif = "formato\\LEYENDA_v2.tif"
# Verificar si la capa de leyenda ya existe en el mxd
layers_in_mxd = [layer.name for layer in arcpy.mapping.ListLayers(mxd)]
# Cargar capa de leyenda
if "LEYENDA_v2.tif" not in layers_in_mxd:
    if os.path.exists(ruta_leyenda_tif):
        try:
            legend.autoAdd = True
            capa_leyenda = arcpy.mapping.Layer(ruta_leyenda_tif)
            arcpy.mapping.AddLayer(df, capa_leyenda, "BOTTOM")
            capa_leyenda.visible = False
            print("LEYENDA_v2.tif añadido al mxd.")
        except Exception as e:
            print("Error cargando capa de leyenda: {}".format(e))
else:
    print("LEYENDA_v2.tif ya está en el mxd.")
ruta_lagos_lyr = "formato/glaciares_y_lagos/Lagos.lyr"
layers_in_mxd = [layer.name for layer in arcpy.mapping.ListLayers(mxd)]

# Cargar capa de Lagos desde el archivo .lyr
if "Lagos" not in layers_in_mxd:  
    if arcpy.Exists(ruta_lagos_lyr):  # Verifica si el archivo .lyr realmente existe
        try:
            legend.autoAdd = True
            capa_lagos = arcpy.mapping.Layer(ruta_lagos_lyr)
            arcpy.mapping.AddLayer(df, capa_lagos, "BOTTOM")
            print("Lagos.lyr añadido al mxd.")
        except Exception as e:
            print("Error cargando capa de lagos: {}".format(e))
else:
    print("La capa 'Lagos' ya está en el mxd.")
#fin archivos leyenda

# Cargar comunas shp
for region in regiones.keys():
    R = region
    ruta_comunas_shp = "shape\\comunas\\{}.shp".format(R)
    
    # Verificar si la capa ya existe en el mxd
    capa_existe = arcpy.mapping.ListLayers(mxd, R, df)
    
    if capa_existe:
        layer = capa_existe[0]
        if os.path.exists(ruta_comunas_shp):
            try:
                # Reemplazar el origen de datos de la capa existente
                layer.replaceDataSource(os.path.dirname(ruta_comunas_shp), "SHAPEFILE_WORKSPACE", os.path.basename(ruta_comunas_shp), False)
                print("Origen de datos de {}.shp actualizado".format(R))
                
                # Aplicar el estilo desde el archivo .lyr a la capa leyenda.tif
                ruta_estilo = "formato\\comunas\\comunas_anomalia.lyr"
                sourceLayer = arcpy.mapping.Layer(ruta_estilo)
                arcpy.mapping.UpdateLayer(df, layer, sourceLayer, True)
                print("Estilo comuna aplicado a {}".format(R))
            
            except Exception as e:
                print("Error actualizando capa para la region {}: {}".format(R, e))
    
    else:
        print("{}.shp no está en el mxd".format(R))

# Cargar capa Glaciares
layers_in_mxd = [layer.name for layer in arcpy.mapping.ListLayers(mxd)]

for region in regiones.keys():
    ruta_glaciares_shp = "shape/glaciares/Glaciares_{}.shp".format(region)
    layer_name = "Glaciares_{}".format(region)

    # Verificar si la capa ya existe en el mxd
    if layer_name not in layers_in_mxd:
        if os.path.exists(ruta_glaciares_shp):
            try:
                capa_glaciares = arcpy.mapping.Layer(ruta_glaciares_shp)
                arcpy.mapping.AddLayer(df, capa_glaciares, "BOTTOM")
                capa_glaciares.visible = False
                print("Glaciares_{}.shp añadido".format(region))

                # Aplicar el estilo desde el archivo .lyr a la capa leyenda.tif
                glaciar_layer = arcpy.mapping.ListLayers(mxd, layer_name)[0]
                ruta_estilo = "formato/glaciares_y_lagos/Glaciares2.lyr" 
                sourceLayer = arcpy.mapping.Layer(ruta_estilo)
                arcpy.mapping.UpdateLayer(df, glaciar_layer, sourceLayer, True)
                print("estilo glaciares aplicado")

            except Exception as e:
                print("Error cargando capa  Glaciares para la region {}: {}".format(region, e))
        else:
            print("No se encontró el archivo Glaciares_{}.shp".format(region))
    else:
        print("Glaciares_{}.shp ya está en el mxd".format(region))


# Cargar lagos 
for region in regiones.keys():
    R = region
    ruta_lagos_shp = "shape\\lagos\\Lagos_{}.shp".format(R)

    # Verificar si la capa de lagos ya existe en el mxd
    layers_in_mxd = [layer.name for layer in arcpy.mapping.ListLayers(mxd)]
    layer_name = "Lagos_{}".format(R)

    if layer_name not in layers_in_mxd:
        if os.path.exists(ruta_lagos_shp):
            try:
                capa_lagos = arcpy.mapping.Layer(ruta_lagos_shp)
                arcpy.mapping.AddLayer(df, capa_lagos, "BOTTOM")
                capa_lagos.visible = False
                print("Lagos_{}.shp añadido".format(R))

                 # Aplicar el estilo desde el archivo .lyr a la capa leyenda.tif
                Lagos_layer = arcpy.mapping.ListLayers(mxd, "Lagos_{}".format(R))[0]
                ruta_estilo = "formato/glaciares_y_lagos/Lagos.lyr" 
                sourceLayer = arcpy.mapping.Layer(ruta_estilo)
                arcpy.mapping.UpdateLayer(df, Lagos_layer, sourceLayer, True)
                print("estilo glaciares aplicado")
            except Exception as e:
                print("Error cargando capa de lagos para la region {}: {}".format(R, e))
    else:
        print("Lagos_{}.shp ya está en el mxd".format(R))

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
legend.autoAdd = False

# Cargar capa de indice vegetacional.tif
for region in regiones.keys():
    R = region
    ruta_anomalia_tif = "data\\{0}\\TIF\\ANOMALIA\\{0}_Anomalia_{1}_median_ZA.tif".format(R,veg_index)
    if os.path.exists(ruta_anomalia_tif):
        try:
            capa_anomalia = arcpy.mapping.Layer(ruta_anomalia_tif)
            arcpy.mapping.AddLayer(df, capa_anomalia, "BOTTOM")
            capa_anomalia.visible=False
            print("tif {} añadido".format(R))
        except Exception as e:
            print("Error cargando capa {} para la region {}: {}".format(veg_index,R, e))

# Cargar capa Regional
if "Regional" not in layers_in_mxd:
    if os.path.exists("shape/chile/Regional.shp"):
        try:
            capa_regional = arcpy.mapping.Layer("shape/chile/Regional.shp")
            arcpy.mapping.AddLayer(df, capa_regional, "BOTTOM")
            capa_regional.visible = True
            print("Regional.shp añadido al mxd.")
        except Exception as e:
            print("Error cargando capa Regional: {}".format(e))
else:
    print("Regional.shp ya está en el mxd.")


# Hacer todas las capas invisibles
layers = arcpy.mapping.ListLayers(mxd, "", df)
for layer in layers:
    try:
        layer.visible = False
    except Exception as e:
        print("Error con la capa: {}. Error: {}".format(layer.name,e))

arcpy.RefreshActiveView()
arcpy.RefreshTOC()

# Extraer solo los nombres y ordenar la lista alfabéticamente
layer_names = sorted([layer.name for layer in arcpy.mapping.ListLayers(mxd)])

# Filtrar y almacenar los nombres de las capas que contienen "Anomalia_NDVI o SAVI"
anomalia_layers = [name for name in layer_names if "Anomalia_{}".format(veg_index) in name]
# Contar y mostrar los nombres de las capas
anomalia_count = len(anomalia_layers)
print(anomalia_count)
print(anomalia_layers)
#indice begetacional AÑADIDO

#Aplicar estilo a Regiones(Chile)
Regional_layer = arcpy.mapping.ListLayers(mxd, "Regional")[0]
Regional_layer.visible = False
ruta_estilo = "formato/Regional/Regional.lyr"
sourceLayer = arcpy.mapping.Layer(ruta_estilo)
arcpy.mapping.UpdateLayer(df, Regional_layer, sourceLayer, True)

# Aplicar el estilo desde el archivo .lyr a la capa leyenda.tif
leyenda_layer = arcpy.mapping.ListLayers(mxd, "LEYENDA_v2.tif")[0]
leyenda_layer.visible = False
ruta_estilo = "formato/ANOMALIA/LEYENDA_TIF.lyr"
sourceLayer = arcpy.mapping.Layer(ruta_estilo)
arcpy.mapping.UpdateLayer(df, leyenda_layer, sourceLayer, True)


def aplicar_simbologia(region):
    capa_destino = "{}_Anomalia_{}_median_ZA.tif".format(region,veg_index)
    target_layers = arcpy.mapping.ListLayers(mxd, capa_destino)
    try:
        if target_layers:
            target_layer = target_layers[0]
            arcpy.mapping.UpdateLayer(df, target_layer, sourceLayer, True)
            #arcpy.ApplySymbologyFromLayer_management(target_layer, leyenda_layer)
            print("simbologia aplicada en {}".format(region))
        else:
            print("No se encontró la capa destino {}".format(capa_destino))
    except Exception as e:
        print("error al aplicar simbologia en region {}".format(region))        


def remover_capa_glaciares():
    # Encuentra y elimina la capa "Glaciares" si existe
    for lyr in arcpy.mapping.ListLayers(mxd, "Glaciares"):
        arcpy.mapping.RemoveLayer(df, lyr)
        arcpy.RefreshActiveView()


remover_capa_glaciares()
def agregar_capa_leyenda(region):
    if region in ["R10","R11","R12"]:
        legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
        legend.autoAdd = True
        ruta_glaciares = "formato/glaciares_y_lagos/Glaciares2.lyr"
        glaciares_layer = arcpy.mapping.Layer(ruta_glaciares)
        
        arcpy.mapping.AddLayer(df, glaciares_layer,"BOTTOM")
        arcpy.RefreshActiveView()
        print("leyenda glaciares añadida")


def proceso(region):
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
    legend.autoAdd = True
    aplicar_simbologia(region)
    remover_capa_glaciares()
    # Establecer la visibilidad y el zoom basado de la región
    layer_principal_list = arcpy.mapping.ListLayers(mxd, region)
    if layer_principal_list:
        layer_principal = layer_principal_list[0]
        arcpy.RefreshActiveView()
        
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        df.extent = layer_principal.getExtent()
        arcpy.RefreshActiveView()
        
        layer_principal.visible = False  # Desactivar la visibilidad después del zoom
        arcpy.RefreshActiveView()
    else:
        print("No se encontró la capa principal {}".format(region))
        return

    if region == "R13":
        capas = [layer.name for layer in arcpy.mapping.ListLayers(mxd) if layer.name == "R13"]
    else:
        capas = [region]

    capas.extend(["{}_Anomalia_{}_median_ZA.tif".format(region,veg_index), "Lagos_{}".format(region)])
    
    #ACTIVA CAPA GLACIARES
    if region in [ "R10","R11", "R12"]:
        capas.append("Glaciares_{}".format(region))

    for capa in capas:
        layer_list = arcpy.mapping.ListLayers(mxd, capa)
        if layer_list:
            layer = layer_list[0]
            layer.visible = True
            arcpy.RefreshActiveView()
        else:
            print("No se encontró la capa {}".format(capa))

    agregar_capa_leyenda(region)
    # Actualiza el título
    titulo_nuevo = "Anomalia de {} del {}, {}".format(veg_index,regiones[region],fecha)
    for elem in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if "Anomalia" in elem.text:
            elem.text = titulo_nuevo
            break

# Asegurarse de que la capa "Regional" está visible
    regional_layers = arcpy.mapping.ListLayers(mxd, "Regional")
    if regional_layers:
        regional_layer = regional_layers[0]
        regional_layer.visible = True
        arcpy.RefreshActiveView()
    else:
        print("Capa 'Regional' no encontrada.")
    # Guarda el PNG
    carpeta_region = os.path.join("export", region)

    if not os.path.exists(carpeta_region):
        os.makedirs(carpeta_region)

    # Crear subcarpeta NDVI o SAVI
    carpeta = os.path.join(carpeta_region, "{}".format(veg_index))
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    arcpy.RefreshActiveView()  # Refrescar la vista antes de guardar el PNG
    salida_png = os.path.join(carpeta, "{}_ANOMALIA_{}.png".format(region,veg_index))
    arcpy.mapping.ExportToPNG(mxd, salida_png, resolution=300, background_color="255, 255, 255")
    print("png {} guardado".format(region))

    # Ocultar todas las capas de la región actual después de guardar el PNG
    for capa in capas:
        layer_list = arcpy.mapping.ListLayers(mxd, capa)
        if layer_list:
            layer = layer_list[0]
            layer.visible = False
            arcpy.RefreshActiveView()


if veg_index=="NDVI":
    for region in regiones.keys():
        if region != "R01" and region != "R02" and region != "R15":
            proceso(region)
        else: print ("{} se calcula con SAVI".format(region))
    print("Script finalizado, veg_index=NDVI")

elif veg_index=="SAVI":
    proceso("R01")
    proceso("R02")
    proceso("R15")
    print("Script finalizado, veg_index=SAVI")

mxd.save()