# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Cellular automata library and application setup.py """

from setuptools import setup, find_packages

from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Cellular Automata',

    version='0.1.0',

    description='A cellular automata library and application',
    long_description=long_description,
    url='https://github.com/enthought/ets-examples/cellular-automata',
    author='Corran Webster',
    author_email='info@enthought.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    keywords='example traits traitsui gui enable chaco cellular automata life',
    packages=find_packages(),
    install_requires=[
        'scipy',
        'pillow>=3.1',
    ],
    extras_require={
        'examples': ['click', 'joblib', 'matplotlib'],
    },
    entry_points={
        'gui_scripts': [],
    },
)
