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

os.chdir("D:/mapas_boletin/mapas_boletin")
mxd = arcpy.mapping.MapDocument("ANOMALIA_SAVI3.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layers = arcpy.mapping.ListLayers(mxd, "", df)


legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
legend.autoAdd = False

for layer in layers:
    if layer.isRasterLayer and layer.name != "LEYENDA_v2.tif":
        arcpy.mapping.RemoveLayer(df, layer)
        print("{} removida".format(layer.name))

# Cargar capa SAVI.tif
for region in regiones.keys():
    R = region
    ruta_anomalia_SAVI_tif = "data\\{0}\\TIF\\ANOMALIA\\{0}_Anomalia_SAVI_median_ZA.tif".format(R)
    if os.path.exists(ruta_anomalia_SAVI_tif):
        try:
            capa_anomalia = arcpy.mapping.Layer(ruta_anomalia_SAVI_tif)
            arcpy.mapping.AddLayer(df, capa_anomalia, "BOTTOM")
            capa_anomalia.visible=False
            print("tif {} añadido".format(R))
        except Exception as e:
            print("Error cargando capa para la region {}: {}".format(R, e))

# Cargar regiones shp
for region in regiones.keys():
    R = region
    ruta_comunas_shp = "shape\\comunas\\{}.shp".format(R)
    if os.path.exists(ruta_comunas_shp):
        try:
            capa_lagos = arcpy.mapping.Layer(ruta_comunas_shp)
            arcpy.mapping.AddLayer(df, capa_lagos, "BOTTOM")
            capa_lagos.visible=False
            print("{}.shp añadido".format(R))
        except Exception as e:
            print("Error cargando capa para la region {}: {}".format(R, e))

#cargar lagos 
for region in regiones.keys():
    R = region
    ruta_comunas_shp = "shape\\lagos\\Lagos_{}.shp".format(R)
    if os.path.exists(ruta_comunas_shp):
        try:
            capa_lagos = arcpy.mapping.Layer(ruta_comunas_shp)
            arcpy.mapping.AddLayer(df, capa_lagos, "BOTTOM")
            capa_lagos.visible=False
            print("Lagos_{}.shp añadido".format(R))
        except Exception as e:
            print("Error cargando capa para la region {}: {}".format(R, e))


# Hacer todas las capas invisibles
layers = arcpy.mapping.ListLayers(mxd, "", df)
for layer in layers:
    try:
        layer.visible = False
    except Exception as e:
        print("Error con la capa: {}. Error: {}".format(layer.name,e))

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
ruta_leyenda_tif = "formato\\LEYENDA_v2.tif"
try:
    leyenda_tif_layer = arcpy.mapping.Layer(ruta_leyenda_tif)
    arcpy.mapping.AddLayer(df, leyenda_tif_layer)
except Exception as e:
    print("Error cargando la capa LEYENDA_v2.tif: {}".format(e))
    # Detiene la ejecución si hay un error al cargar la capa
    exit()

arcpy.RefreshActiveView()
arcpy.RefreshTOC()

legend.autoAdd = True
# Aplicar el estilo desde el archivo .lyr a la capa leyenda.tif
leyenda_layer = arcpy.mapping.ListLayers(mxd, "LEYENDA_v2.tif")[0]
leyenda_layer.visible = False
ruta_estilo = "formato\\ANOMALIA\\LEYENDA_TIF.lyr"
sourceLayer = arcpy.mapping.Layer(ruta_estilo)
arcpy.mapping.UpdateLayer(df, leyenda_layer, sourceLayer, True)



def aplicar_simbologia(region):
    capa_destino = "{}_Anomalia_SAVI_median_ZA.tif".format(region)
    target_layers = arcpy.mapping.ListLayers(mxd, capa_destino)
    
    if target_layers:
        target_layer = target_layers[0]
        arcpy.ApplySymbologyFromLayer_management(target_layer, leyenda_layer)
        print("simbologia aplicada")
    else:
        print("No se encontró la capa destino {}".format(capa_destino))


def remover_capa_glaciares():
    # Encuentra y elimina la capa "Glaciares" si existe
    for lyr in arcpy.mapping.ListLayers(mxd, "Glaciares"):
        arcpy.mapping.RemoveLayer(df, lyr)
        arcpy.RefreshActiveView()
    
    # Paso 5: Desactivar el añadido automático de capas a la leyenda
    # Suponemos que solo hay una leyenda en el mxd y la obtenemos
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
    legend.autoAdd = False


remover_capa_glaciares()
def agregar_capa_leyenda(region):
    if region in ["R11", "R12"]:
        # Paso 1: Añadir la capa "Glaciares" al documento de mapa
        ruta_glaciares = r"formato\glaciares y lagos\Glaciares.lyr"
        glaciares_layer = arcpy.mapping.Layer(ruta_glaciares)
        
        # Añadimos la capa "Glaciares" al fondo del marco de datos
        arcpy.mapping.AddLayer(df, glaciares_layer, "BOTTOM")

        # Paso 2: Asegurarnos que la capa se añade automáticamente a la leyenda
        # Suponemos que solo hay una leyenda en el mxd y la obtenemos
        legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
        
        # Habilitamos el añadido automático de capas a la leyenda
        legend.autoAdd = True

        # Paso 3: Actualizar el mxd para reflejar los cambios
        arcpy.RefreshActiveView()
        print("pase por aqui")


def proceso(region):
    aplicar_simbologia(region)
    remover_capa_glaciares()
    # Establecer la visibilidad y el zoom basado en la capa principal de la región
    layer_principal_list = arcpy.mapping.ListLayers(mxd, region)
    if layer_principal_list:
        layer_principal = layer_principal_list[0]
        layer_principal.visible = True
        layer_principal.visible = True
        arcpy.RefreshActiveView()
        
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        df.extent = layer_principal.getExtent()
        arcpy.RefreshActiveView()
        
        #layer_principal.visible = False  # Desactivar la visibilidad después del zoom
        arcpy.RefreshActiveView()
    else:
        print("No se encontró la capa principal {}".format(region))
        return

    if region == "R13":
        capas = [layer.name for layer in arcpy.mapping.ListLayers(mxd) if layer.name == "R13"]
    else:
        capas = [region]

    capas.extend(["{}_Anomalia_SAVI_median_ZA.tif".format(region), "Lagos_{}".format(region)])
    
    if region in ["R11", "R12"]:
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
    agregar_capa_leyenda(region)

    # Actualiza el título
    titulo_nuevo = "Anomalia de SAVI del 26 de junio al 11 de julio de 2023, {}".format(regiones[region])
    for elem in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if "Anomalia" in elem.text:
            elem.text = titulo_nuevo
            break

    # Guarda el PNG
    carpeta_region = os.path.join("export", region)

    if not os.path.exists(carpeta_region):
        os.makedirs(carpeta_region)

    # Crear subcarpeta SAVI
    carpeta_savi = os.path.join(carpeta_region, "SAVI")
    if not os.path.exists(carpeta_savi):
        os.makedirs(carpeta_savi)
    
    arcpy.RefreshActiveView()  # Refrescar la vista antes de guardar el PNG
    salida_png = os.path.join(carpeta_savi, "{}_ANOMALIA_SAVI.png".format(region))
    arcpy.mapping.ExportToPNG(mxd, salida_png, resolution=300, background_color="255, 255, 255")
    print("png region {} guardado".format(region))

    # Ocultar todas las capas de la región actual después de guardar el PNG
    for capa in capas:
        layer_list = arcpy.mapping.ListLayers(mxd, capa)
        if layer_list:
            layer = layer_list[0]
            layer.visible = False
            arcpy.RefreshActiveView()

    # Asegurarse de que la capa "Regional" está visible
    regional_layers = arcpy.mapping.ListLayers(mxd, "Regional")
    if regional_layers:
        regional_layer = regional_layers[0]
        regional_layer.visible = True
        arcpy.RefreshActiveView()
    else:
        print("Capa 'Regional' no encontrada.")


#Ejecutar el proceso para cada región
#for region in regiones.keys():
 #   proceso(region)
proceso("R15")
proceso("R01")
proceso("R02")
proceso("R15")

print("Script finalizado.")

##falta añadir leyenda, desactivas todo antes de comenzar el script menos regiones 