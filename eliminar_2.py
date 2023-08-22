# -*- coding: utf-8 -*-

import arcpy

# Definir el documento de mapa
mxd = arcpy.mapping.MapDocument("C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\ANOMALIA_SAVI.mxd")

# Establecer la geodatabase como el espacio de trabajo
arcpy.env.workspace = "C:\\Users\\INIA\\Desktop\\MAPA_ANOMALIA_PYTHON\\Geodatabase.gdb"

# Definir el dataframe y las capas
df = arcpy.mapping.ListDataFrames(mxd)[0]
layers = arcpy.mapping.ListLayers(mxd)
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
legend.autoAdd = True

# Añadir la capa al mapa
leyenda_lyr_path = r"C:\Users\INIA\Desktop\MAPA_ANOMALIA_PYTHON\formato\ANOMALIA\LEYENDA_TIF.lyr"
leyenda_layer_from_lyr = arcpy.mapping.Layer(leyenda_lyr_path)
arcpy.mapping.AddLayer(df, leyenda_layer_from_lyr, "TOP")

# Copiar los datos subyacentes de LEYENDA_TIF.lyr a Geodatabase.gdb
if leyenda_layer_from_lyr.supports("DATASOURCE"):
    data_source_path = leyenda_layer_from_lyr.dataSource
    output_feature_class = "LEYENDA_TIF"
    output_path = r"C:\Users\INIA\Desktop\MAPA_ANOMALIA_PYTHON\Geodatabase.gdb\{}".format(output_feature_class)
    arcpy.CopyFeatures_management(data_source_path, output_path)
    print("Capa {} ha sido añadida a la geodatabase.".format(output_feature_class))
else:
    print("El archivo .lyr no tiene una fuente de datos asociada.")

# Guardar el mapa
mxd.save()
