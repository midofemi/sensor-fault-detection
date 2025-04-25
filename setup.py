from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str = "requirements.txt") -> List[str]:
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]
        return requirements

setup(
    name="sensor",
    version="0.0.1",
    author="Amidu Kamara",
    author_email="midofemi@yahoo.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
