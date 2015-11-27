#!/usr/bin/env python
# encoding: utf8
from __future__ import (absolute_import, print_function, division, unicode_literals)

from crypto_enigma import __version__


def pytest_report_header(config):
    return "version: {}".format(__version__)