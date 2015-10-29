#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of Crypto-Enigma, the Enigma Machine simulation.
# Crypto-Enigma is released under the BSD-3 License (see License.txt).


""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

from distutils.core import setup
from os.path import join, dirname

import enigma

setup(
    name='crypto-enigma',
    version=enigma.__version__,
    author='Roy Levien',
    author_email='royl@aldaron.com',
    url='http://www.aldaron.com',
    license='BSD',
    description='An Enigma machine simulation library.',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    packages=['enigma', 'enigma.tests'],
    # package_data=dict(enigma=['examples/*.py',
    #                           'docs/source/*.rst',
    #                           'docs/source/*.py',
    #                          ]),
    scripts=[],
    #scripts=['test.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)


