import os
def windows():
    # Set the path to lammps executable
    lmppath = None # <--- Set the path to lammps executable here



    if lmppath is None:

        file_path = os.path.join(os.path.dirname(__file__), __file__)

        intro = "\n" + 80*"=" + "\n"
        msg = "\n In windows this package can't install automatically. \n Lammps path must be set manually.\n For example: lmppath = 'C:\\path\\to\\lmp.exe'. \n Go to file: {}".format(file_path) + " and set the path manually.\n"
        raise Exception(intro + msg + intro)

    return lmppath