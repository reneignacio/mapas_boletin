# -*- coding: utf-8 -*-
import arcpy
import os

mxd = arcpy.mapping.MapDocument("C:\\Users\\INIA\\Desktop\\Agosto\\ANOMALIA_SAVI_AGOSTO_v2.mxd")

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
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
legend.autoAdd = False

df = arcpy.mapping.ListDataFrames(mxd)[0]

for region in regiones.keys():
    R=regiones.keys()

    Anomalia_region=f"C:\Users\INIA\Desktop\2023-06-26_v2\{R}\TIF\ANOMALIA\{R}_Anomalia_SAVI_median_ZA.tif"

    arcpy.mapping.AddLayer(df,Anomalia_region)



leyenda_layer = arcpy.mapping.ListLayers(mxd, "LEYENDA")[0]
def aplicar_simbologia(region):
    capa_destino = "{}_Anomalia_SAVI_median_ZA.tif".format(region)
    target_layers = arcpy.mapping.ListLayers(mxd, capa_destino)
    
    if target_layers:
        target_layer = target_layers[0]
        arcpy.ApplySymbologyFromLayer_management(target_layer, leyenda_layer)
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
        ruta_glaciares = r"C:\Users\INIA\Desktop\Agosto\ANOMALIA_NDVI\Glaciares.lyr"
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
    carpeta_region = os.path.join("C:\\Users\\INIA\\Desktop\\Agosto\\anomalias", region)

    if not os.path.exists(carpeta_region):
        os.makedirs(carpeta_region)

    # Crear subcarpeta SAVI
    carpeta_savi = os.path.join(carpeta_region, "SAVI")
    if not os.path.exists(carpeta_savi):
        os.makedirs(carpeta_savi)
    
    arcpy.RefreshActiveView()  # Refrescar la vista antes de guardar el PNG
    salida_png = os.path.join(carpeta_savi, "{}_ANOMALIA_SAVI.png".format(region))
    arcpy.mapping.ExportToPNG(mxd, salida_png, resolution=300, background_color="255, 255, 255")


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
proceso("R01")
proceso("R02")
proceso("R15")

print("Script finalizado.")

