import os
import subprocess
from  .manage_install import manage_install

lmp = manage_install()

def check_gpu_count():
    """Check the number of available GPUs using nvidia-smi."""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            gpu_list = result.stdout.decode().strip().split('\n')
            return len(gpu_list)
    except FileNotFoundError:
        # nvidia-smi not found, assume no GPUs
        pass
    return 0

def runlmp(infile,outfolder, OMP_NUM_THREADS=1, mpi=1, use_gpu=True):
    """Run LAMMPS simulation with optional GPU support."""
    
    os.environ["OMP_NUM_THREADS"] = str(OMP_NUM_THREADS)

    curr = os.getcwd()  # Save current directory
    os.chdir(outfolder)  # Change to output folder

    outfolder_abs = os.path.abspath(outfolder)
    gpu_count = check_gpu_count() if use_gpu else 0  # Get GPU count if GPU usage is enabled

    try:
        # Base LAMMPS command
        cmd = f"{lmp} -in {infile} > log.lammps"
        
        # Adjust for MPI
        if mpi > 1:
            cmd = f"mpirun --oversubscribe -np {mpi} {cmd}"
        
        # Add GPU option if GPUs are available
        if gpu_count > 0:
            cmd = f"{cmd} -sf gpu -pk gpu {gpu_count}"

        print(f"Running LAMMPS with command: \n{cmd}\nIn folder: {outfolder_abs}")
        os.system(cmd)  # Execute command
    except Exception as e:
        print(f"Error running LAMMPS: {e}")
    finally:
        os.chdir(curr)  # Restore original directory

