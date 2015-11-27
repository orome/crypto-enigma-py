#!/usr/bin/env python
# encoding: utf8

""" 
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

# See - http://www.python.org/dev/peps/pep-0440/
# See - http://semver.org
__author__ = 'Roy Levien'
__copyright__ = '(c) 2014-2015 Roy Levien'
__release__ = '0.2.1'  # N(.N)*
__pre_release__ = 'b1'  # aN | bN | cN |
__suffix__ = '.dev4'  # .devN | | .postN
__version__ = __release__ + __pre_release__ + __suffix__


