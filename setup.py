from setuptools import setup, find_packages

setup(
    name="speciestrack",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.1.2",
        "requests>=2.32.5",
    ],
)
