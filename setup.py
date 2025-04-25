from setuptools import find_packages,setup #This library (find_packages) would search the root directory (Sensor_Detection_Project) and 
                                           # would find the sensor folder because inside of it, we have a __init__.py file. Now you see
                                           #why we have __init__.py inside of the sensor folder. That how the library will locate that folder
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    return requirement_list

setup(
    name="sensor", #Folder name that house our packages
    version="0.0.1",
    author="MidoINC",
    author_email="midofemi@yahoo.com",
    packages = find_packages(), #We are calling the library above to find the packages in the folder sensor
    install_requires=["pymongo==4.2.0"]#get_requirements(),#Here we are just taking all the libraries from requirements.txt. So this is how it will look like.
                                        #["pymongo==4.2.0","pandas""ETC ETC"], 
)
