import os
from djlmp.installLammps import installLammps
import zipfile

join = os.path.join

folder_file   =  join(os.path.dirname(__file__))
folder_lmp    =  join(folder_file, "lammps")
lmp_linux_bin =  join(folder_file, "bin")
lmp_linux_lib =  join(lmp_linux_bin,"lmp")
lmp_linux_zip =  join(lmp_linux_bin,"lmp.zip")
def manage_install():
    
    if os.name == "nt":
        from djlmp.windows import windows
        lmp = windows()

    else:
        # comprobe is DJLMP_LAMMPS exist
        if "DJLMP_LAMMPS" in os.environ:
            lmp = os.environ["DJLMP_LAMMPS"]
            # check if the path is correct
            # also lmp can be a command
        else:

            if not os.path.exists(lmp_linux_lib):
                with zipfile.ZipFile(lmp_linux_zip, "r") as zip_ref:
                    zip_ref.extractall(lmp_linux_bin)
            # executable permissions
            os.chmod(lmp_linux_lib, 0o755)

            cmd = lmp_linux_lib + "  -help > /dev/null 2>&1"
            if os.system(cmd) == 0:
                print("Lammps found in: "+lmp_linux_lib)
                lmp = lmp_linux_lib
            else:   
                if not os.path.exists(folder_lmp):
                    print("Its the first time you run this code, so we need to install lammps")
                    installLammps(folder_file)
                print("Lammps not found in: "+lmp_linux_lib)
                lmp = os.path.join(folder_lmp,"build","lmp")
    
    return lmp