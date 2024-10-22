import os
import shutil
import requests
from tqdm import tqdm

# Lista de paquetes predeterminados
pkgs_default = ["PKG_MOLECULE", "PKG_CLASS2", "PKG_KSPACE", 
                "PKG_COMPRESS", "PKG_MANYBODY", "PKG_MC",
                "PKG_QEQ", "PKG_USER-INTEL", 
                "PKG_USER-MISC",
                "PKG_FEP",
                "PKG_USER-OMP",  
                "PKG_EXTRA-PAIR","PKG_DPD-BASIC"]

def download_with_progress(url, output_path):
    """Descargar un archivo con una barra de progreso."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # Tamaño del bloque en bytes
    
    with open(output_path, 'wb') as file, tqdm(
        total=total_size, unit='B', unit_scale=True, desc=output_path, ncols=80
    ) as progress_bar:
        for data in response.iter_content(block_size):
            file.write(data)
            progress_bar.update(len(data))

def installLammps(folder_target, pkgs=pkgs_default):
    """Instalar LAMMPS con una barra de progreso para la descarga y compilación."""
    lammps_url = "https://github.com/lammps/lammps/archive/refs/heads/stable.zip"
    lmpzipfile = os.path.join(folder_target, "stable.zip")

    # Descargar LAMMPS con una barra de progreso
    print("Descargando LAMMPS...")
    download_with_progress(lammps_url, lmpzipfile)

    # Descomprimir el archivo descargado
    print("\nDescomprimiendo el archivo...")
    shutil.unpack_archive(lmpzipfile, folder_target, "zip")
    os.remove(lmpzipfile)

    lmfile = "lammps-stable"  # Nombre de la carpeta descomprimida
    shutil.move(os.path.join(folder_target, lmfile), 
                os.path.join(folder_target, "lammps"))

    # Comando de compilación
    cmd = f"cd {folder_target}/lammps && mkdir build && cd build && "

    cmd_cmake = "cmake ../cmake/"
    for pkg in pkgs:
        cmd_cmake += f" -D {pkg}=yes"

    cmd += cmd_cmake + " && make -j4"
    cmd += " > build.log 2> build.err"
    
    # Ejecutar el comando de compilación y mostrar progreso simulado
    print("\nCompilando LAMMPS, esto puede tomar unos minutos...")
    with tqdm(total=100, desc="Compilando LAMMPS", ncols=80) as progress_bar:
        os.system(cmd)

    print("Instalación completada.")


def installLammpsindjl(pkgs=pkgs_default,force=False):

    
    
    folder_target = os.path.dirname(os.path.abspath(__file__))
    
    # if exist folder lammps return 
    exist_lammps = os.path.exists(os.path.join(folder_target, "lammps"))
    if exist_lammps:
        if force:
            shutil.rmtree(os.path.join(folder_target, "lammps"))
        else:
            print("LAMMPS ya está instalado en la carpeta actual.")
            return


    installLammps(folder_target, pkgs)