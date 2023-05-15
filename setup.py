#!/usr/bin/env python

import os

from distutils.core import setup
from setuptools import find_packages


BASE = os.path.dirname(__file__)
README = os.path.join(BASE, 'README.rst')
with open(README) as f:
    LONG_DESCRIPTION = f.read()
REQUIREMENTS = os.path.join(BASE, 'requirements.txt')
with open(REQUIREMENTS, 'r') as f:
    INSTALL_REQUIRES = f.readlines()


setup(
    name='responses_server',
    version='0.1.1',
    description='Unit testing HTTP server based on responses library.',
    long_description=LONG_DESCRIPTION,
    install_requires=INSTALL_REQUIRES,
    author='Ben Timby',
    author_email='btimby@gmail.com',
    url='https://github.com/btimby/cesium.tv/responses_server/',
    packages=find_packages(),
)
