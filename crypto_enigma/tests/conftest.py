#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

# REV - This has no effect - http://stackoverflow.com/q/18558666/656912
def pytest_report_header(config):
    return "Testing Enigma functionality"
