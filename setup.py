#!/usr/bin/env python

# Setup script for the `cnelib' package.
#
# Author: Ismael Lugo <ismaelrlgv@gmail.com>
# Last Change: 06-04-2016
# URL: https://github.com/IsmaelRLG/cnelib

import sys
import codecs
import os

# De-facto standard solution for Python packaging.
from setuptools import find_packages, setup

# Find the directory where the source distribution was unpacked.
source_directory = os.path.dirname(os.path.abspath(__file__))

# Add the directory with the source distribution to the search path.
sys.path.append(source_directory)

# Fill in the long description (for the benefit of PyPI)
# with the contents of README.rst (rendered by GitHub).
readme_file = os.path.join(source_directory, 'README.rst')
with codecs.open(readme_file, 'r', 'utf-8') as handle:
    readme_text = handle.read()

import cnelib

setup(
    name='cnelib',
    version=cnelib.__version__,
    description='Libreria para consultas del Consejo Nacional Electoral (CNE)',
    long_description=readme_text,
    author='Ismael Lugo',
    author_email='ismaelrlgv@gmail.com',
    url='https://github.com/IsmaelRLG/cnelib',
    #install_requires=['TorCtl'],
    scripts=['bin/cne'],
    packages=find_packages(),
    classifiers=[
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Spanish',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Operating System :: OS Independent'
    ]
)
