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

""" To-do list application setup.py """

from setuptools import setup, find_packages

from codecs import open
from os import path

from babel.messages import frontend as babel

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Internationalized To-do list',

    version='0.1.0',

    description='An TraitsUI to-do list application with i18n',
    long_description=long_description,
    url='https://github.com/enthought/ets-examples/todo-list',
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
    keywords='example traits traitsui gui i18n internationalization',
    cmdclass = {
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog,
    },
    packages=find_packages(),
    install_requires=['traitsui>=5.1', 'babel'],
    extras_require={
        'wx': ['wxpython>=2.8.10', 'numpy'],
        'pyqt': ['pyqt>=4.10', 'pygments'],
        'pyside': ['pyside>=1.2', 'pygments'],
    },
    entry_points={
        'gui_scripts': [
            'todo-list-i18n=todo_list.app:main',
        ],
    },
    package_data={
        'todo_list': ['translations/*/*/*.mo'],
    }
)
