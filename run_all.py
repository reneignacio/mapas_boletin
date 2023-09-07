import os
import arcpy

os.chdir("C:/Users/Marcel/Desktop/mapas_boletin/mapas_boletin/")
os.system('python anom_NDVI_Y_SAVI.py &')
os.system('python dif_NDVI_Y_SAVI.py &')
os.system('python NDVI_Y_SAVI.py &')
os.system('VCI.py &')
