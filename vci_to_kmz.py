# -*- coding: utf-8 -*-

import arcpy

# Habilitar la sobrescritura de archivos existentes
arcpy.env.overwriteOutput = True

# Obtener el mapa actualmente abierto en ArcMap
mxd = arcpy.mapping.MapDocument("C:/Users/Marcel/Desktop/mapas_boletin/mapas_boletin/vci_shape.mxd")

# Obtener la primera vista de datos del mapa
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Ruta del archivo .lyr que quieres aplicar a todas las capas
lyr_file = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\formato\\VCI\\VCI_shp.lyr"
lyr_to_apply = arcpy.mapping.Layer(lyr_file)

# Carpeta donde se guardarán los archivos .kmz
kmz_folder = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\export\\vci_kmz\\"

# Añadir y simplificar cada shapefile antes de exportar a .kmz
for i in range(1, 17):  # Desde 1 a 16
    region = "R{:02d}".format(i)  # R01, R02, ..., R16
    shp_path = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\data\\{0}\\SHP\\VCI\\{0}_VCI.shp".format(region)
    
    # Verificar si el archivo existe
    if arcpy.Exists(shp_path):
        
        # Determinar la tolerancia de simplificación según la región
        tolerance = 200 if region in ['R11', 'R12'] else 5
        
        # Simplificar el shapefile
        simplified_shp = "in_memory\\{}_simplified".format(region)
        arcpy.SimplifyPolygon_cartography(shp_path, simplified_shp, "POINT_REMOVE", tolerance, error_option="NO_CHECK")
        
        # Añadir la capa simplificada al mapa
        new_layer = arcpy.mapping.Layer(simplified_shp)
        arcpy.mapping.AddLayer(df, new_layer)
        
        # Aplicar el archivo .lyr
        added_layer = arcpy.mapping.ListLayers(mxd, new_layer.name, df)[0]
        arcpy.mapping.UpdateLayer(df, added_layer, lyr_to_apply, True)
        
        # Exportar a .kmz
        kmz_file = "{}{}_VCI.kmz".format(kmz_folder, region)
        arcpy.LayerToKML_conversion(added_layer, kmz_file)
        
    else:
        print("El archivo {} no existe.".format(shp_path))

# Refrescar el mapa para ver los cambios
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
