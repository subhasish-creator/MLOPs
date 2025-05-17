from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements=f.read().splitlines()


setup(
    name="Hotel_Room_Prediction",
    version="0.1",
    author="Subhasish",
    packages=find_packages(),
    install_requires=requirements,
)

#D:\MLOPS\setup.py