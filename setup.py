from setuptools import setup, find_packages

setup(
    name="RosComm",                
    version="0.1.0",                 
    author="Somil Agrawal",
    author_email="somil0014@gmail.com",
    description="A simple package to communicate with ESP32",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),        
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.1",
    install_requires=[
        "pyserial",
    ],
)
