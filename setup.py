# it helps to create build this project as a package
# its a configuration for that having all meta data about 

from setuptools import find_packages,setup

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> list:
    '''Return list of requirements from a requirements file.'''
    requirements: list = []
    with open(file_path) as file_obj:
        requirements = [req.strip() for req in file_obj.readlines() if req.strip()]
        #### IN PYTHON EMPTY LINES EVALUATES TO FALSE #####
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
    

setup(
    name = "mlproject",
    version = "0.0.1",
    author="sarthak",
    author_email="sarthaktomar345@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)