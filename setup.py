# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='alis',
    version='0.0.3',
    description='ALIS API Python Client',
    long_description=readme,
    author='hoosan',
    url='https://github.com/alisista/py-alis',
    license=license,
    packages=find_packages(),
    install_requires=[
        "promise",
        "requests",
        "warrant"
    ]
)

