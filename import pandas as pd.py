import pandas as pd
from datetime import datetime, timedelta
import os

# Función para convertir día juliano y hora en fecha y hora reales
def julian_to_datetime(julian_day, hour, year=2010):
    date = datetime(year, 1, 1) + timedelta(julian_day - 1, hours=hour)
    return date

# Función para extraer los datos de una estación específica de un archivo
def extract_station_data(file_path, station_name):
    df = pd.read_csv(file_path)
    # Convertir día juliano y hora en fecha y hora
    df['fecha_hora'] = df.apply(lambda row: julian_to_datetime(row['dia_juliano'], row['hora']), axis=1)
    # Seleccionar solo las columnas de fecha_hora y de la estación específica
    if station_name in df.columns:
        df = df[['fecha_hora', station_name]]
        df = df.rename(columns={station_name: file_path.split('_')[1]})
    else:
        df = pd.DataFrame(columns=['fecha_hora', file_path.split('_')[1]])
    return df

# Directorio donde se encuentran tus archivos CSV
directory = "D:\\heladas_v2\\datos_nuevos\\unidos\\procesado\\resultado"

# Lista de nombres de archivos
file_names = [
    'pp_acum_rellenado.csv',
    'rsi_rellenado.csv',
    'temp_rellenado.csv',
    'vel_viento_rellenado.csv',
    'dir_med_rellenado.csv',
    'hr_med_rellenado.csv',
    'pb_rellenado.csv'
]

# Lista de estaciones
stations = ["INIA.58", "INIA.59", "INIA.60"]  # Añade aquí todas las estaciones

# Procesamiento para cada estación
for station in stations:
    combined_data = None
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        station_data = extract_station_data(file_path, station)
        if combined_data is None:
            combined_data = station_data
        else:
            combined_data = pd.merge(combined_data, station_data, on='fecha_hora', how='outer')
    # Rellenar valores faltantes con NA
    combined_data.fillna('NA', inplace=True)
    # Guardar a CSV
    output_path = os.path.join(directory, f'{station}_data.csv')
    combined_data.to_csv(output_path, index=False)
