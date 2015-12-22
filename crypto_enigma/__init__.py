#!/usr/bin/env python
# encoding: utf8

"""An Enigma machine simulator with rich textual display functionality.

Limitations
~~~~~~~~~~~

Note that the correct display of some characters used to represent
components (thin Naval rotors) assumes support for Unicode, while some
aspects of the display of machine state depend on support for combining
Unicode. This is a `known
limitation <https://github.com/orome/crypto-enigma-py/issues/1>`__ that
will be addressed in a future release.

Note also that at the start of any scripts that use this package, you should

.. parsed-literal::

   from __future__ import unicode_literals

before any code that uses the API, or confiure IPython (in `ipython_config.py`) with

.. parsed-literal::

   c.InteractiveShellApp.exec_lines += ["from __future__ import unicode_literals"]

or explicitly suppply Unicode strings (e.g., as in many of the examples here with :code:`u'TESTING'`).

"""

from ._version import __version__, __author__
#__all__ = ['machine', 'components']

from .components import *
from .machine import *
