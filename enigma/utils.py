#!/usr/bin/env python
# encoding: utf8

"""
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

import time
import sys


# TBD - Generalize to other platforms; test?
def print_over(s, delay=0.2):
    print(s, end='\r')
    print("\033[F" * (s.count('\n')+1))
    sys.stdout.flush()
    time.sleep(delay)


def num_A0(c):
    return ord(c) - ord('A')


def chr_A0(n):
    return chr(n + ord('A'))


def ordering(items):
    return [i[1] for i in sorted(zip(items, range(0, len(items))))]


# standard simple-substitution cypher encoding
def encode_char(mapping, ch):
    if ch == ' ':
        return ' '
    else:
        return mapping[num_A0(ch)]


def encode_string(mapping, string):
    return ''.join([encode_char(mapping, ch) for ch in string])


# scan, because it's missing from Python; implemented to anticipate Python 3
def accumulate(l, f):
    it = iter(l)
    total = next(it)
    yield total
    for element in it:
        total = f(total, element)
        yield total

# also missing from Python
def chunk_of(it, n):
    return [it[i:i+n] for i in range(0, len(it), n)]
