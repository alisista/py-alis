# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='alis',
    version='0.0.4',
    description='ALIS API Python Client',
    long_description_content_type="text/x-rst",
    long_description=readme,
    author='hoosan',
    author_email='hoosanalis@gmail.com',
    url='https://github.com/alisista/py-alis',
    license=license,
    packages=find_packages(),
    install_requires=[
        "promise",
        "requests",
        "warrant"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)

