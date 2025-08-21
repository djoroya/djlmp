import os
from  .manage_install import manage_install

lmp = manage_install()

def runlmp(namefile,output_folder,OMP_NUM_THREADS=1,mpi=False,mpi_np=4):
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
        if mpi:
            mpirun = "mpirun -np {} ".format(mpi_np)
        else:
            mpirun = ""
        # error file error.lammps
        cmd = mpirun + lmp+" -in "+ namefile + " > out.lammps 2> msg.lammps"

        # show cmd
        long = len(cmd)

        print(long*"="+ "\n")
        print(" output: "+os.path.join(abs_out,"out.lammps"))
        print("\n cmd   : "+cmd+"\n")
        print(long*"=")

        error = os.system(cmd)

    os.chdir(curr)
    return error,cmd