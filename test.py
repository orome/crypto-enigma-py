#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)
""" Simple test file for debugging and testing at the shell. To use simply
        python test.py
    or
        ./test.py
    or run "test" in PyCharm.
"""

# import cProfile
#
# import euler
# cProfile.run('euler.euler046()')

#import sys
#for p in sys.path:
#    print p

import enigma

ec = enigma.EnigmaConfig("c-γ-I-VIII-III", "UYZO", "UX.MI", "03.22.04.09")
print(ec.components)
print(ec.rings)
print(ec.positions)
print(ec.stages)
# print(ec._window_letter(1))
# print(ec._window_letter(2))
# print(ec._window_letter(3))
# st = 2
# print(ec._window_letter(st))
# print(enigma.component(ec.components[st]).turnovers)
# print(ec._window_letter(st) in enigma.component(ec.components[st]).turnovers)

print([str(ec.windows())] + [str(ec.step().windows()) for _ in xrange (99)])

# print(ec.windows())
# for i in range(99):
#     ec.step()
#     print(ec.windows())
