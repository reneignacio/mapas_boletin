import os
import paramiko

archivos_transferidos = 0
errores_transferencia = 0

def obtener_ruta_destino(codigo, directorio, regiones):
    base_path = f"/var/www/LaravelInia/public/photos/shares/2023/Septiembre/{regiones[codigo]}/"
    if directorio == "NDVI":
        return f"{base_path}Análisis Del Indice De Vegetación Normalizado (NDVI)/"
    if directorio == "SAVI":
        return f"{base_path}Análisis Del Índice De Vegetación Ajustado al Suelo (SAVI)/"
    if directorio == "componente_meteorologico": #"componente_meteorologico/plot"
        return f"{base_path}Componente Meteorológico/"
    if directorio == "SOIL_MOISTURE":
        return f"{base_path}Disponibilidad de Agua/"
    if directorio == "VCI":
        return f"{base_path}Indice De Condición De La Vegetación (VCI) (En Evaluación)/"

def copiar_imagenes(ssh, sftp, codigo, ruta_base_local, regiones, directorio):
    global archivos_transferidos, errores_transferencia
    
    ruta_local_region = os.path.join(ruta_base_local, codigo, directorio)
    
    if not os.path.exists(ruta_local_region):
        print(f"Directorio {ruta_local_region} no encontrado. Saltando...")
        return

    archivos = [f for f in os.listdir(ruta_local_region) if os.path.isfile(os.path.join(ruta_local_region, f)) and f.endswith('.png')]
    
    ruta_destino = obtener_ruta_destino(codigo, directorio, regiones)

    # En tu función copiar_imagenes
    for archivo in archivos:
        ruta_imagen_local = os.path.join(ruta_local_region, archivo)
        ruta_imagen_destino = os.path.join(ruta_destino, archivo)
        
        print(f"Intentando transferir desde {ruta_imagen_local} a {ruta_imagen_destino}")
        
        try:
            sftp.put(ruta_imagen_local, ruta_imagen_destino)
            archivos_transferidos += 1
            print(f"Imagen {archivo} copiada a {ruta_destino}")
        except FileNotFoundError:
            errores_transferencia += 1
            print(f"Archivo {archivo} no encontrado en {ruta_imagen_local}.")
        except Exception as e:
            errores_transferencia += 1
            print(f"Error desconocido al copiar la imagen {archivo}: {e}")


def main():
    host = "186.64.122.224"
    port = 22222
    user = "root"
    passwd = "pzQ35tLoPNBSl5990m"
    
    regiones = {
        "R01" : "Tarapacá", "R02" : "Antofagasta","R03" : "Atacama",
        "R04": "Coquimbo", "R05": "Valparaíso", "R06": "OHiggins", "R07": "Maule",
        "R08": "Bío Bío", "R09": "Araucanía", "R10": "Los Lagos",
        "R11": "Aysén", "R12": "Magallanes", "R13": "Metropolitana", "R14": "Los Rios",
        "R15": "Arica y Parinacota", "R16": "Ñuble"
    }

#RECUERDA CREAR CARPETA OHiggins todos los meses

    ruta_base_local = "C:/Users/Marcel/Desktop/mapas_boletin/mapas_boletin/export"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=user, password=passwd)
    sftp = ssh.open_sftp()
    
    for codigo, region in regiones.items():
        if codigo in ["R01", "R02", "R15"]:
           copiar_imagenes(ssh, sftp, codigo, ruta_base_local, regiones, 'SAVI')
        if codigo not in ["R01", "R02", "R15"]:
            copiar_imagenes(ssh, sftp, codigo, ruta_base_local, regiones, 'NDVI')
        if codigo in ["R05", "R06", "R07", "R08", "R09", "R13", "R16"]:  
            copiar_imagenes(ssh, sftp, codigo, ruta_base_local, regiones, 'SOIL_MOISTURE')

        #copiar_imagenes(ssh, sftp, codigo, ruta_base_local, regiones, 'componente_meteorologico')
        copiar_imagenes(ssh, sftp, codigo, ruta_base_local, regiones, 'VCI')
    sftp.close()
    ssh.close()

    # Resumen
    print(f"\n{archivos_transferidos} archivos transferidos con éxito.")
    print(f"{errores_transferencia} errores al transferir archivos.")

if __name__ == "__main__":
    main()
