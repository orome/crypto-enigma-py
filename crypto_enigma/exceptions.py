#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

"""
This module defines some placeholders for custom exceptions and errors.

.. todo::
    Document.
"""


from __future__ import (absolute_import, print_function, division, unicode_literals)


# Placeholder exceptions
class EnigmaError(Exception):
    pass


class EnigmaValueError(EnigmaError, ValueError):
    pass


class EnigmaDisplayError(EnigmaError):
    pass