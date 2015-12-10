#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

"""
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

import time
import sys


# TBD - Generalize to other platforms; test?
def print_over(s, backup=True, delay=0.2):
    if backup:
        print('', end='\r')
        print("\033[F" * (s.count('\n')+2))
    print(s)
    sys.stdout.flush()
    time.sleep(delay)



def ordering(items):
    return [i[1] for i in sorted(zip(items, range(0, len(items))))]


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

from functools import wraps
# require unicode strings (see unicode_literal in enigma.py)
#   http://stackoverflow.com/a/33743668/656912
#   http://code.activestate.com/recipes/454322-type-checking-decorator/
def require_unicode(*given_arg_names):
    def check_types(_func_):
        @wraps(_func_)
        def modified(*args, **kwargs):
            arg_names = list(_func_.func_code.co_varnames[:_func_.func_code.co_argcount])
            if len(given_arg_names) == 0:
                # ASK - Where should this be; it should really happen when the decorator is applied <<<
                raise TypeError('No arguments provided to require_unicode decorator.')
                #unicode_arg_names = arg_names
            else:
                unicode_arg_names = given_arg_names
            for unicode_arg_name in unicode_arg_names:
                try:
                    arg_index = arg_names.index(unicode_arg_name)
                    if len(args) > arg_index:
                        arg = args[arg_index]
                    elif unicode_arg_name in kwargs:
                        arg = kwargs[unicode_arg_name]
                    else:
                        # Not given as argument, even though in list
                        continue
                    if not isinstance(arg, unicode):
                        raise TypeError("Parameter '{}' should be Unicode".format(unicode_arg_name))
                except ValueError:
                    raise NameError(unicode_arg_name)
            return _func_(*args, **kwargs)
        return modified
    return check_types

