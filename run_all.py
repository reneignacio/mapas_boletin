import os
import arcpy

os.chdir("C:/Users/Marcel/Desktop/mapas_boletin/mapas_boletin/")
os.system('python anom_NDVI_Y_SAVI.py &')
os.system('python dif_NDVI_Y_SAVI.py &')
os.system('python NDVI_Y_SAVI.py &')
os.system('python VCI.py &')
#os.system('python soil_moisture.py &')

#se demora aprox 8 min
#resultados se guardan en carpeta "export"