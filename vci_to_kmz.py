# -*- coding: utf-8 -*-
import arcpy
import os

# Obtener el MXD y el dataframe actual
#mxd = arcpy.mapping.MapDocument("VCI_SHP_TO_KMZ.mxd")
mxd = arcpy.mapping.MapDocument("CURRENT")
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

def remove_all_layers(mxd, data_frame):
    for lyr in arcpy.mapping.ListLayers(mxd, "", data_frame):
        arcpy.mapping.RemoveLayer(data_frame, lyr)
    print("Todas las capas existentes han sido eliminadas.")

# Habilitar la sobrescritura de archivos existentes
arcpy.env.overwriteOutput = True

# Función para eliminar campos innecesarios
def delete_unnecessary_fields(shp_path, fields_to_keep):
    fields = arcpy.ListFields(shp_path)
    fields_to_delete = [f.name for f in fields if f.name not in fields_to_keep and f.required == False]
    
    if fields_to_delete:
        arcpy.DeleteField_management(shp_path, fields_to_delete)
        print("Campos innecesarios eliminados.")
    else:
        print("No hay campos innecesarios para eliminar.")

def apply_lyr_to_one_shapefile(mxd, df, lyr_file, output_shp_path, region):
    lyr_to_apply = arcpy.mapping.Layer(lyr_file)
    new_layer = arcpy.mapping.Layer(output_shp_path)  # Crea una nueva capa desde el shapefile
    arcpy.mapping.AddLayer(df, new_layer)  # Añade la nueva capa al data frame
    
    layer_list = arcpy.mapping.ListLayers(mxd, "{}_output".format(region), df)  # Modificado para buscar por region
    if layer_list:
        added_layer = layer_list[0]
        arcpy.mapping.UpdateLayer(df, added_layer, lyr_to_apply, True)
        print("Estilo .lyr aplicado a la capa {}.".format(region))
    else:
        print("No se pudo encontrar la capa {} para aplicar el estilo.".format(region))

def find_layer_by_name(layer_name, layer_list):
    for layer in layer_list:
        if layer.name == layer_name:
            return layer
    return None

# Rutas de las carpetas y otros recursos
data_folder_path = r"C:\Users\Marcel\Desktop\mapas_boletin\mapas_boletin\data"
output_folder = r"C:\Users\Marcel\Desktop\mapas_boletin\mapas_boletin\export\output"
layer_file_path = r"C:\Users\Marcel\Desktop\mapas_boletin\mapas_boletin\formato\VCI\VCI_shp_para_kmz.lyr"
kmz_output_folder = r"C:\Users\Marcel\Desktop\mapas_boletin\mapas_boletin\export\vci_kmz"

# Campos a conservar
fields_to_keep = ['nom_com', 'VCI']


# Eliminar todas las capas existentes
print("Eliminando todas las capas existentes...")
remove_all_layers(mxd, data_frame)

# Ruta de la carpeta donde están los archivos .shp
folder_path = r"C:\Users\Marcel\Desktop\mapas_boletin\mapas_boletin\shape\comunas_simplificado"
data_folder_path = r"C:\Users\Marcel\Desktop\mapas_boletin\mapas_boletin\data"


# Primero, cargar los archivos .shp de la carpeta inicial
for filename in os.listdir(folder_path):
    if filename.endswith(".shp"):
        full_path = os.path.join(folder_path, filename)
        arcpy.mapping.AddLayer(data_frame, arcpy.mapping.Layer(full_path))

# Luego, cargar los archivos .shp de las carpetas R01 hasta R16
for i in range(1, 17):
    region = "R{:02d}".format(i)
    shp_file_name = "{}_VCI.shp".format(region)
    shp_full_path = os.path.join(data_folder_path, region, "SHP", "VCI", shp_file_name)
    
    if os.path.exists(shp_full_path):
        arcpy.mapping.AddLayer(data_frame, arcpy.mapping.Layer(shp_full_path))
    else:
        print ("No se encontró el archivo .shp en la ruta: {}".format(shp_full_path))

print ("Shapefiles añadidos con éxito.")


# Procesar cada región desde R01 hasta R16 (1,17)
for i in range(1, 17):

    region = "R{:02d}".format(i)
    original_shp_name = "{}_VCI".format(region)
    simplified_shp_name = "{}_simplificado".format(region)
    output_shp_name = "{}_output".format(region)
    kmz_output_name = "{}_VCI.kmz".format(region)

    output_shp_path = os.path.join(output_folder, output_shp_name + ".shp")
    kmz_output_path = os.path.join(kmz_output_folder, kmz_output_name)

 # Comprobar si las capas necesarias existen en el MXD
    layers = arcpy.mapping.ListLayers(mxd, "*", data_frame)
    original_layer = find_layer_by_name(original_shp_name, layers)
    simplified_layer = find_layer_by_name(simplified_shp_name, layers)
    
    if original_layer and simplified_layer:
        # Unión y copia de campos
        arcpy.JoinField_management(simplified_layer, "nom_com", original_layer, "nom_com", ["A2023"])
        arcpy.CalculateField_management(simplified_layer, "VCI", "!A2023!", "PYTHON_9.3")
        arcpy.DeleteField_management(simplified_layer, "A2023")

        # Crear nuevo shapefile
        arcpy.CopyFeatures_management(simplified_layer, output_shp_path)

        # Eliminar campos innecesarios
        delete_unnecessary_fields(output_shp_path, fields_to_keep)

        # Añadir la nueva capa al MXD
        #new_layer = arcpy.mapping.Layer(output_shp_path)
        #arcpy.mapping.AddLayer(data_frame, new_layer)

        # Añadir la nueva capa al MXD y aplicar simbología con la función
        apply_lyr_to_one_shapefile(mxd, data_frame, layer_file_path, output_shp_path, region)  # Paso el output_shp_path

        #exportar a kmz
        layer_list = arcpy.mapping.ListLayers(mxd, output_shp_name, data_frame)
        if layer_list:
            layer_to_export = layer_list[0]
            arcpy.LayerToKML_conversion(layer_to_export, kmz_output_path)
            print("Procesamiento completado para la región {}".format(region))
        else:
            print("No se encontró la capa con el nombre {} en el MXD actual.".format(output_shp_name))



print("Todos los procesos han terminado exitosamente.")
