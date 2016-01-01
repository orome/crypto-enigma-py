#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015-2016 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).


""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

from os.path import join, dirname

import crypto_enigma

from setuptools import setup

# TBD - Add Licence and changelog; see -- https://github.com/RIPE-NCC/ripe-atlas-tools/blob/master/README.rst <<<

# read_me = "Crypto-Enigma"
# try:
#     from pypandoc import convert
#     read_md = lambda f: convert(f, b'rst')
#     read_me = read_md('README.md')
# except ImportError:
#     print("warning: pypandoc module not found, could not convert Markdown to RST")
#     read_me = open(join(dirname(__file__), 'README.rst')).read()
# _DEV_STATUS = {'a': '3 - Alpha',
#                'b': '4 - Beta',
#                'c': '5 - Production/Stable'}['c' if enigma.__pre_release__ == '' else enigma.__pre_release__[0]]

setup(name=b'crypto-enigma',
      version=crypto_enigma.__version__,
      author=crypto_enigma.__author__,
      author_email='royl@aldaron.com',
      url='https://github.com/orome/crypto-enigma-py',
      license='BSD',
      description='An Enigma machine simulation package.',
      long_description=open(join(dirname(__file__), 'README.rst')).read(),
      packages=[b'crypto_enigma'],
      # package_data=dict(enigma=['examples/*.py',
      #                           'docs/source/*.rst',
      #                           'docs/source/*.py']),
      scripts=['enigma.py','pyenigma.py'],
      # scripts=['test.py'],
      classifiers=['Development Status :: {}'.format('4 - Beta'),
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Other Audience',
                   'Intended Audience :: Education',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Topic :: Security :: Cryptography',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities',
                   'Natural Language :: English'])
