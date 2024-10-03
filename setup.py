from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Sobrescribir el comando de instalación para incluir la instalación de LAMMPS"""
    
    def run(self):
        # Llama a la función de instalación de LAMMPS
        print("Instalando LAMMPS...")
        folder_target = os.path.join(os.getcwd(), "src", "dependencies")
        if not os.path.exists(folder_target):
            os.makedirs(folder_target)
        

        print("Instalando LAMMPS en {}".format(folder_target))

        # Continúa con la instalación normal del paquete
        install.run(self)

setup(
    name="djlmp",
    version="0.1.0",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Deyviss Jesús Oroya Villalta",
    author_email="djoroya@gmail.com",
    url="https://github.com/djoroya/djlmp",
    packages=find_packages(),
    project_urls={
        "Source Code": "https://github.com/djoroya/djlmp",
        "Bug Tracker": "https://github.com/djoroya/djlmp/issues",
    },
    # from requeriments.txt
    install_requires=open('requirements.txt').read().split('\n'),
    python_requires='>=3.6',  # Versión mínima de Python requerida
    classifiers=[  # Clasificadores que ayudan a otros desarrolladores a encontrar tu proyecto
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Tipo de licencia
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
    },
    cmdclass={
        'install': CustomInstallCommand,  # Sobrescribir el comando de instalación
    }
)
