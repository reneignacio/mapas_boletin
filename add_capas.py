import arcpy
# Obtener el mapa actualmente abierto en ArcMap
mxd = arcpy.mapping.MapDocument("CURRENT")

# Obtener la primera vista de datos del mapa
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Ruta del archivo .lyr que quieres aplicar a todas las capas
lyr_file = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\formato\\VCI\\VCI_shp.lyr"
lyr_to_apply = arcpy.mapping.Layer(lyr_file)

# Añadir cada shapefile al mapa y aplicar el estilo del archivo .lyr
for i in range(1, 17):  # Desde 1 a 16
    region = "R{:02d}".format(i)  # R01, R02, ..., R16
    shp_path = "C:\\Users\\Marcel\\Desktop\\mapas_boletin\\mapas_boletin\\data\\{0}\\SHP\\VCI\\{0}_VCI.shp".format(region)
    
    # Verificar si el archivo existe antes de añadirlo
    if arcpy.Exists(shp_path):
        new_layer = arcpy.mapping.Layer(shp_path)
        arcpy.mapping.AddLayer(df, new_layer)
        
        # Obtener la capa recién añadida para aplicarle el archivo .lyr
        added_layer = arcpy.mapping.ListLayers(mxd, new_layer.name, df)[0]
        arcpy.mapping.UpdateLayer(df, added_layer, lyr_to_apply, True)

    else:
        print "El archivo {0} no existe.".format(shp_path)

# Refrescar el mapa para ver los cambios
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
