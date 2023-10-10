import paramiko

def replicar_estructura_directorios(sftp, origen, destino, mes):
    origen_completo = f"/var/www/LaravelInia/public/photos/shares/2023/{mes}/{origen}"
    destino_completo = f"/var/www/LaravelInia/public/photos/shares/2023/{mes}/{destino}"

    # Crear la carpeta de destino si no existe
    try:
        sftp.mkdir(destino_completo)
    except IOError as e:
        print(f"El directorio {destino_completo} ya existe o no se pudo crear: {e}")

    print(f"Origen completo: {origen_completo}")  # Para depuración
    # Obtener la lista de subdirectorios en el directorio de origen
    lista_subdirs = sftp.listdir(origen_completo)

    # Crear esos mismos subdirectorios en el directorio de destino
    for subdir in lista_subdirs:
        origen_subdir = f"{origen_completo}/{subdir}"
        destino_subdir = f"{destino_completo}/{subdir}"

        # Verificar si es un directorio
        try:
            if sftp.stat(origen_subdir).st_mode & 0o40000:  # Comprobar si es un directorio
                try:
                    sftp.mkdir(destino_subdir)
                except IOError as e:
                    print(f"El subdirectorio {destino_subdir} ya existe o no se pudo crear: {e}")
        except IOError as e:
            print(f"No se pudo obtener información del subdirectorio {origen_subdir}: {e}")

def main():
    host = "186.64.122.224"
    port = 22222
    user = "root"
    passwd = "pzQ35tLoPNBSl5990m"  # Cambia esto por tu contraseña real

    mes = "Octubre"  # Puedes cambiar esto según necesites

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=user, password=passwd)
    sftp = ssh.open_sftp()

    replicar_estructura_directorios(sftp, "O`Higgins", "OHiggins", mes)

    sftp.close()
    ssh.close()

if __name__ == "__main__":
    main()
