#!/usr/bin/env python
# encoding: utf8

""" The CE package (this is in init).  """

from ._version import __version__, __author__
#__all__ = ['machine', 'components']

from .components import *
from .machine import *
