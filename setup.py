#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script de instalación para cnelib
#------------------------------------------
#
# Autor: Ismael Lugo <ismaelrlgv@gmail.com>
# Ultimo cambio: 2017-05-20
# URL: https://github.com/IsmaelRLG/cnelib

import os
import cnelib

from setuptools import find_packages, setup
current_dir = os.path.dirname(os.path.abspath(__file__))
readme_file = os.path.join(current_dir, 'README.rst')
with file(readme_file, 'r') as fp:
    readme_text = fp.read()
requires = file(os.path.join(current_dir, 'requirements.txt'), 'r')
requires = requires.read().splitlines()

setup(
    name='cnelib',
    version=cnelib.__version__,
    description='Libreria para consultas sobre el Consejo Nacional Electoral (CNE)',
    long_description=readme_text,
    author='Ismael Lugo',
    author_email='ismaelrlgv@gmail.com',
    license='MIT',
    url='https://github.com/IsmaelRLG/cnelib',
    install_requires=requires,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    entry_points=dict(console_scripts=[
        'cedula = cnelib.cnelib_cli:main',
        #'cne2cedula = cnelib.migrate:main',
        ])
)
