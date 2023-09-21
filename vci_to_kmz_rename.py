
import arcpy
import os

def remove_all_layers(mxd, df):
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        arcpy.mapping.RemoveLayer(df, lyr)
    print("Todas las capas existentes han sido eliminadas.")

# Habilitar la sobrescritura de archivos existentes
arcpy.env.overwriteOutput = True

def load_shapefiles(mxd, df):
    for i in range(1, 17):  # Desde 1 a 16
        region = "R{:02d}".format(i)
        shp_path = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\data\\{0}\\SHP\\VCI\\{0}_VCI.shp".format(region)

        if arcpy.Exists(shp_path):
            new_layer = arcpy.mapping.Layer(shp_path)
            arcpy.mapping.AddLayer(df, new_layer)
            print("Capa {} añadida.".format(region))
        else:
            print("El archivo {} no existe.".format(shp_path))

def apply_lyr_to_shapefiles(mxd, df, lyr_file):
    lyr_to_apply = arcpy.mapping.Layer(lyr_file)
    for i in range(1, 17):
        region = "R{:02d}".format(i)
        layer_list = arcpy.mapping.ListLayers(mxd, "*_s", df)


        if layer_list:
            added_layer = layer_list[0]
            arcpy.mapping.UpdateLayer(df, added_layer, lyr_to_apply, True)
            print("Estilo .lyr aplicado a la capa {}.".format(region))

def delete_unnecessary_fields(shp_path, fields_to_keep):
    fields = arcpy.ListFields(shp_path)
    fields_to_delete = [f.name for f in fields if f.name not in fields_to_keep and f.required == False]
    
    if fields_to_delete:
        arcpy.DeleteField_management(shp_path, fields_to_delete)
        print("Campos innecesarios eliminados.")
    else:
        print("No hay campos innecesarios para eliminar.")


def rename_field(shp_path, old_field, new_field):
    # Comprobar si el campo antiguo existe
    fields = [f.name for f in arcpy.ListFields(shp_path)]
    if old_field not in fields:
        print("El campo {} ya no existe en la capa. Saltando el renombrado.".format(old_field))
        return

    # Crear un nuevo campo con el nombre nuevo y el mismo tipo del campo antiguo
    old_field_type = arcpy.ListFields(shp_path, old_field)[0].type
    arcpy.AddField_management(shp_path, new_field, old_field_type)
    # Copiar los valores del campo antiguo al nuevo campo
    with arcpy.da.UpdateCursor(shp_path, [old_field, new_field]) as cursor:
        for row in cursor:
            row[1] = row[0]
            cursor.updateRow(row)

    # Eliminar el campo antiguo
    arcpy.DeleteField_management(shp_path, old_field)
    print("Campo {} renombrado a {}.".format(old_field, new_field))


def simplify_shapefiles(mxd, df, tolerance_dict, output_folder):
    fields_to_keep = ['FID', 'Shape', 'nom_com', 'VCI']
    
    for i in range(1, 17):  # Desde 1 a 16
        region = "R{:02d}".format(i)
        shp_path = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\data\\{0}\\SHP\\VCI\\{0}_VCI.shp".format(region)
        simplified_shp_path = os.path.join(output_folder, "{}_VCI_s.shp".format(region))
        
        if arcpy.Exists(shp_path):
            tolerance = tolerance_dict.get(region, 10) 
            arcpy.SimplifyPolygon_cartography(shp_path, simplified_shp_path, "POINT_REMOVE", tolerance, error_option="NO_CHECK")
            delete_unnecessary_fields(simplified_shp_path, fields_to_keep)
            print("Polígono simplificado para la región {} con tolerancia {}.".format(region,tolerance))



def apply_lyr_to_memory_layers(mxd, df, lyr_file):
    lyr_to_apply = arcpy.mapping.Layer(lyr_file)
    for i in range(1, 17):
        region = "R{:02d}".format(i)
        layer_list = arcpy.mapping.ListLayers(mxd, "*_s", df)

        if layer_list:
            added_layer = layer_list[0]
            arcpy.mapping.UpdateLayer(df, added_layer, lyr_to_apply, True)
            print("Estilo .lyr aplicado a la capa simplificada {}.".format(region))


def export_layers_to_kmz(mxd, df, output_folder, simplified_shp_folder):
    for i in range(1, 17):
        region = "R{:02d}".format(i)
        simplified_shp_path = os.path.join(simplified_shp_folder, "{}_VCI_s.shp".format(region))
        
        if arcpy.Exists(simplified_shp_path):
            new_layer = arcpy.mapping.Layer(simplified_shp_path)
            arcpy.mapping.AddLayer(df, new_layer)
            
            output_kmz_path = os.path.join(output_folder, "{}_VCI.kmz".format(region))
            arcpy.LayerToKML_conversion(new_layer, output_kmz_path)
            print("Capa simplificada {} exportada como KMZ.".format(region))
        else:
            print("La capa simplificada {} no está presente en el mapa.".format(region))




def delete_unnecessary_fields_from_simplified(output_folder, fields_to_keep):
    for i in range(1, 17):  # Desde 1 a 16
        region = "R{:02d}".format(i)
        simplified_shp_path = os.path.join(output_folder, "{}_VCI_s.shp".format(region))
        
        if arcpy.Exists(simplified_shp_path):
            delete_unnecessary_fields(simplified_shp_path, fields_to_keep)
            print("Campos innecesarios eliminados de la capa simplificada {}_VCI_s.".format(region))



# Diccionario de tolerancias para cada región
tolerance_dict = {
    'R11': 200,
    'R12': 200
    # Añade más si es necesario
}

# Habilitar la sobrescritura de archivos existentes
arcpy.env.overwriteOutput = True

# Obtener el mapa actualmente abierto en ArcMap
mxd = arcpy.mapping.MapDocument("CURRENT")

# Obtener la primera vista de datos del mapa
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Ruta del archivo .lyr
lyr_file = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\formato\\VCI\\VCI_shp_para_kmz.lyr"

# Eliminar todas las capas existentes
print("Eliminando todas las capas existentes...")
remove_all_layers(mxd, df)


# Ejecutar la función para cargar los shapefiles
print("Paso 1: Cargando shapefiles...")
load_shapefiles(mxd, df)

# Refrescar el mapa para ver los cambios
arcpy.RefreshActiveView()
arcpy.RefreshTOC()


# Ejecutar la función para cambiar el nombre del campo
print("Paso 2: Cambiando el nombre del campo A2023 a VCI...")
for i in range(1, 17):  # Desde 1 a 16
    region = "R{:02d}".format(i)
    shp_path = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\data\\{0}\\SHP\\VCI\\{0}_VCI.shp".format(region)
    
    if arcpy.Exists(shp_path):
        rename_field(shp_path, 'A2023', 'VCI')

# Refrescar el mapa para ver los cambios
arcpy.RefreshActiveView()
arcpy.RefreshTOC()


# Lista de campos a conservar
fields_to_keep = ['nom_com', 'VCI']

# Paso 3: Eliminar campos innecesarios
print("Paso 3: Eliminando campos innecesarios...")
for i in range(1, 17):
    region = "R{:02d}".format(i)
    shp_path = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\data\\{0}\\SHP\\VCI\\{0}_VCI.shp".format(region)
    
    if arcpy.Exists(shp_path):
        delete_unnecessary_fields(shp_path, fields_to_keep)

# Refrescar el mapa para ver los cambios
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

# Paso 4: Aplicar estilos .lyr
print("Paso 4: Aplicando .lyr...")
apply_lyr_to_shapefiles(mxd, df, lyr_file)

# Refrescar el mapa para ver los cambios
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

# Ruta de la carpeta donde se guardarán los archivos KMZ
output_kmz_folder = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\export\\vci_kmz"

# Ruta de la carpeta donde se guardarán los shapefiles simplificados
simplified_shp_folder = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\export\\vci_kmz_poligonos_simpificados"

# Paso 5: Simplificar shapefiles (Opcional)
print("Paso 5: Simplificando shapefiles (Opcional)...")
simplify_shapefiles(mxd, df, tolerance_dict, output_kmz_folder) 

# Paso 5.1: Eliminar campos innecesarios de las capas simplificadas
print("Paso 5.1: Eliminando campos innecesarios de las capas simplificadas...")
delete_unnecessary_fields_from_simplified(output_kmz_folder, fields_to_keep)

# Paso 6: Aplicar .lyr a capas en memoria
print("Paso 6: Aplicando .lyr a las capas simplificadas...")
apply_lyr_to_memory_layers(mxd, df, lyr_file)

# Paso 7: Exportar capas a KMZ
print("Paso 7: Exportando capas simplificadas a KMZ...")
export_layers_to_kmz(mxd, df, output_kmz_folder, simplified_shp_folder)  # Asumiendo que los shapefiles simplificados también están en output_kmz_folder

# Fin del script
