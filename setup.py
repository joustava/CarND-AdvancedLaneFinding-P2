from setuptools import find_packages, setup

setup(
    name="alf",
    version="0.1",
    package_dir={'': 'scr'},
    packages=find_packages(where='src'),
    # install_requires=[],
)
