#!/usr/bin/env python
# encoding: utf8

"""An Enigma machine simulator with rich textual display functionality for Python 2.7.

Currently support is only provided for those `machine models`_ in most
widespread general use during the war years: the `I`_, `M3`_, and `M4`_.

No attempt is made here to describe the operation of an Enigma machine. For information about how
an Enigma machine works see the excellent and extensive resources available at the
`Crypto Museum`_.

.. _functionality_api:

Functionality and use
~~~~~~~~~~~~~~~~~~~~~

The package provides functionality for :ref:`generating a machine configuration <config_creation>`
from a conventional specification, :ref:`examining the state <config_state>` of a configuration, simulating
the :ref:`operation <config_operation>` of a machine by stepping between states, and
:ref:`encoding messages <config_encoding>`:

Create a machine configuration (see the `~.machine.EnigmaConfig.config_enigma_from_string`):

.. parsed-literal::

    >>> from crypto_enigma import *
    >>> cfg = EnigmaConfig.config_enigma_from_string('B-I-III-I EMO UX.MO.AY 13.04.11')

Encode messages (see the `~.machine.EnigmaConfig.enigma_encoding`):

.. parsed-literal::

    >>> cfg.enigma_encoding('TESTINGXTESTINGUD')
    'OZQKPFLPYZRPYTFVU'

    >>> cfg.enigma_encoding('OZQKPFLPYZRPYTFVU')
    'TESTINGXTESTINGUD'

Show configuration details (see the `~.machine.EnigmaConfig.config_string`):

.. parsed-literal::

    >>> print(cfg.config_string(letter='X', format='internal', mark_func=lambda c: '(' + c + ')'))
    X > ABCDEFGHIJKLMNOPQRSTUVW(X)YZ
      P YBCDEFGHIJKLONMPQRSTXVW(U)AZ         UX.MO.AY
      1 HCZMRVJPKSUDTQOLWEXN(Y)FAGIB  O  05  I
      2 KOMQEPVZNXRBDLJHFSUWYACT(G)I  M  10  III
      3 AXIQJZ(K)RMSUNTOLYDHVBWEGPFC  E  19  I
      R YRUHQSLDPX(N)GOKMIEBFZCWVJAT         B
      3 ATZQVYWRCEGOI(L)NXDHJMKSUBPF         I
      2 VLWMEQYPZOA(N)CIBFDKRXSGTJUH         III
      1 WZBLRVXAYGIPD(T)OHNEJMKFQSUC         I
      P YBCDEFGHIJKLONMPQRS(T)XVWUAZ         UX.MO.AY
    T < CNAUJVQSLEMIKBZRGPHXDFY(T)WO

Simulate machine operation (see the `~.machine.EnigmaConfig.print_operation`):

.. parsed-literal::

    >>> cfg.print_operation(message='TESTING', show_step=True, mark_func=lambda c: '(' + c + ')')
    0000       CNAUJVQSLEMIKBZRGPHXDFYTWO   EMO  19 10 05
    0001  T > UNXKGVERLYDIQBTWMHZ(O)AFPCJS  EMP  19 10 06
    0002  E > QTYJ(Z)XUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
    0003  S > DMXAPTRWKYINBLUESG(Q)FOZHCJV  ENR  19 11 08
    0004  T > IUSMHRPEAQTVDYWGJFC(K)BLOZNX  ENS  19 11 09
    0005  I > WMVXQRLS(P)YOGBTKIEFHNZCADJU  ENT  19 11 10
    0006  N > WKIQXNRSCVBOY(F)LUDGHZPJAEMT  ENU  19 11 11
    0007  G > RVPTWS(L)KYXHGNMQCOAFDZBEJIU  ENV  19 11 12

Watch the machine as it runs for 500 steps:

.. parsed-literal::

    >>> cfg.print_operation(steps=500, show_step=True, format='internal', overwrite=True)

Command line functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~

A command line script, |script_code|, provides access to almost all the functionality of the API.

Encode messages:

.. parsed-literal::

    $ |script| encode "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTINGXTESTINGUD"
    OZQKPFLPYZRPYTFVU

    $ |script| encode "B-I-III-I EMO UX.MO.AY 13.04.11" "OZQKPFLPYZRPYTFVU"
    TESTINGXTESTINGUD

Show configuration details (explained in more detail in the command line help):

.. parsed-literal::

    $ |script| show "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -H'()' -f internal
    X > ABCDEFGHIJKLMNOPQRSTUVW(X)YZ
      P YBCDEFGHIJKLONMPQRSTXVW(U)AZ         UX.MO.AY
      1 HCZMRVJPKSUDTQOLWEXN(Y)FAGIB  O  05  I
      2 KOMQEPVZNXRBDLJHFSUWYACT(G)I  M  10  III
      3 AXIQJZ(K)RMSUNTOLYDHVBWEGPFC  E  19  I
      R YRUHQSLDPX(N)GOKMIEBFZCWVJAT         B
      3 ATZQVYWRCEGOI(L)NXDHJMKSUBPF         I
      2 VLWMEQYPZOA(N)CIBFDKRXSGTJUH         III
      1 WZBLRVXAYGIPD(T)OHNEJMKFQSUC         I
      P YBCDEFGHIJKLONMPQRS(T)XVWUAZ         UX.MO.AY
    T < CNAUJVQSLEMIKBZRGPHXDFY(T)WO

Simulate machine operation (explained in more detail command line help):

.. parsed-literal::

    $ |script| run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()'
    0000       CNAUJVQSLEMIKBZRGPHXDFYTWO   EMO  19 10 05
    0001  T > UNXKGVERLYDIQBTWMHZ(O)AFPCJS  EMP  19 10 06
    0002  E > QTYJ(Z)XUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
    0003  S > DMXAPTRWKYINBLUESG(Q)FOZHCJV  ENR  19 11 08
    0004  T > IUSMHRPEAQTVDYWGJFC(K)BLOZNX  ENS  19 11 09
    0005  I > WMVXQRLS(P)YOGBTKIEFHNZCADJU  ENT  19 11 10
    0006  N > WKIQXNRSCVBOY(F)LUDGHZPJAEMT  ENU  19 11 11
    0007  G > RVPTWS(L)KYXHGNMQCOAFDZBEJIU  ENV  19 11 12

Watch the machine as it runs for 500 steps:

.. parsed-literal::

    $ |script| run  "c-β-VIII-VII-VI QMLI 'UX.MO.AY 01.13.04.11" -s 500 -t -f internal -o

Limitations
~~~~~~~~~~~

Note that the correct display of some characters used to represent
components (thin Naval rotors) assumes support for Unicode, while some
aspects of the display of machine state depend on support for combining
Unicode.
This is a `known limitation <https://github.com/orome/crypto-enigma-py/issues/1>`__
that will be addressed in a future release.

Note also that at the start of any scripts that use this package, you should

.. parsed-literal::

   from __future__ import unicode_literals

before any code that uses the API, or confiure IPython (in `ipython_config.py`) with

.. parsed-literal::

   c.InteractiveShellApp.exec_lines += ["from __future__ import unicode_literals"]

or explicitly supply Unicode strings (e.g., as in many of the examples here with :code:`'TESTING'`).

"""

from ._version import __version__, __author__
#__all__ = ['machine', 'components']

from .components import *
from .machine import *
