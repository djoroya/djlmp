import os
lmp = __file__.replace("run_lmp.py",os.path.join("lammps","lmp_serial"))
# comprobar que lmp existe
if not os.path.isfile(lmp):
    raise Exception("lammps executable not found in {}".format(lmp))

from djlmp.installLammps import installLammps

folder_file_lmp = os.path.join(os.path.dirname(__file__), "lammps")
folder_file = os.path.join(os.path.dirname(__file__))
if not os.path.exists(folder_file_lmp):
    print("Its the first time you run this code, so we need to install lammps")
    installLammps(folder_file)
else:
    print("Lammps already installed")
    lmp = os.path.join(folder_file_lmp,"build","lmp")


def runlmp(output_folder,OMP_NUM_THREADS=1,mpi=False,mpi_np=4):
    """
    Run lammps in a given folder.
    """
    os.environ["OMP_NUM_THREADS"] = str(OMP_NUM_THREADS)

    curr = os.getcwd()
    abs_out = os.path.abspath(output_folder)
    os.chdir(output_folder)

    if os.name == "nt":
        if mpi:
            cmd = "mpiexec -n {} ".format(mpi_np)
            cmd += '"'+lmp+'" -in in.lammps > out.lammps'
        else:   
            cmd = '"'+lmp+'" -in in.lammps > out.lammps'
        print(cmd)
        # show output files path
        print("Output file: "+os.path.join(abs_out,"out.lammps"))
        error = os.system(cmd)
        os.chdir(curr)
    else:
        os.environ["OMP_NUM_THREADS"] = "2"
        np = 4
        mpirun = "mpirun -np {} ".format(np)
        cmd = mpirun+lmp+" -in in.lammps > out.lammps"
        error = os.system(cmd)

    os.chdir(curr)
    return error,cmd