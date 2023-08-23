import arcpy

# Ruta al documento de mapa (MXD)
mxd_path ="ANOMALIA_NDVI.mxd"

# Cargar el documento de mapa
mxd = arcpy.mapping.MapDocument(mxd_path)

# Obtener el primer elemento de tipo leyenda; asumiendo que tienes una leyenda en tu MXD
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]

# Imprimir propiedades del objeto LegendElement
print("autoAdd:", legend.autoAdd)
print("elementHeight:", legend.elementHeight)
print("elementPositionX:", legend.elementPositionX)
print("elementPositionY:", legend.elementPositionY)
print("elementWidth:", legend.elementWidth)
print("isOverflowing:", legend.isOverflowing)
print("items:", ", ".join(legend.items))
print("name:", legend.name)
print("parentDataFrameName:", legend.parentDataFrameName)
print("title:", legend.title)
print("type:", legend.type)

# Limpiar
del mxd
