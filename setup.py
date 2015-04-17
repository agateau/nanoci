#!/usr/bin/env python
# encoding: utf-8
"""
Nanoci, a minimalist continuous integration server

:copyright: 2015 Aurélien Gâteau.
:license: BSD.
"""
import os

from setuptools import setup

import nanoci

DESCRIPTION = 'Minimalist continuous integration server'


setup(name=nanoci.__appname__,
    version=nanoci.__version__,
    description=DESCRIPTION,
    author='Aurélien Gâteau',
    author_email='mail@agateau.com',
    license=nanoci.__license__,
    platforms=['any'],
    url='http://github.com/agateau/nanoci',
    install_requires=[
        'flask',
        'pyyaml',
    ],
    packages=['nanoci'],
    entry_points={
        'console_scripts': [
            'nanoci = nanoci.main:main',
        ],
    }
)
