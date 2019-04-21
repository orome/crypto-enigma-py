crypto-enigma
-------------

|Python Programming Language| |PyPi| |Development Status| |BSD3 License| |PyPi Build Status| |Waffle| |Gitter|

An Enigma machine simulator with state and encoding display for Python 3.6 and 3.7.

Currently support is only provided for those `machine models`_ in most
widespread general use during the war years: the `I`_, `M3`_, and `M4`_.

.. _functionality_api:

Functionality: package API
~~~~~~~~~~~~~~~~~~~~~~~~~~

The package provides functionality for generating a machine configuration
from a conventional specification, examining the state of a configuration, simulating
the operation of a machine by stepping between states, and
encoding messages:

Create a machine configuration (see the `documentation <http://crypto-enigma.readthedocs.org/en/pypi/machine.html#crypto_enigma.machine.EnigmaConfig.config_enigma_from_string>`__ for :code:`config_enigma_from_string`):

.. parsed-literal::

    >>> from crypto_enigma import *
    >>> cfg = EnigmaConfig.config_enigma_from_string(u'B-I-III-I EMO UX.MO.AY 13.04.11')

Encode messages (see the `documentation <http://crypto-enigma.readthedocs.org/en/pypi/machine.html#crypto_enigma.machine.EnigmaConfig.enigma_encoding>`__ for :code:`enigma_encoding`):

.. parsed-literal::

    >>> cfg.enigma_encoding(u'TESTINGXTESTINGUD')
    u'OZQKPFLPYZRPYTFVU'

    >>> cfg.enigma_encoding(u'OZQKPFLPYZRPYTFVU')
    u'TESTINGXTESTINGUD'

Show configuration details (see the `documentation <http://crypto-enigma.readthedocs.org/en/pypi/machine.html#crypto_enigma.machine.EnigmaConfig.config_string>`__ for :code:`config_string`):

.. parsed-literal::

    >>> print(cfg.config_string(letter=u'X', format='internal', mark_func=lambda c: '(' + c + ')'))
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

Simulate machine operation (see the `documentation <http://crypto-enigma.readthedocs.org/en/pypi/machine.html#crypto_enigma.machine.EnigmaConfig.print_operation>`__ for :code:`print_operation`):

.. parsed-literal::

    >>> cfg.print_operation(message=u'TESTING', show_step=True, mark_func=lambda c: '(' + c + ')')
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

.. _functionality_commandline:

Functionality: command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A command line script, |script_code|, provides almost all the functionality of the API.

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

    $ |script| run "c-β-VIII-VII-VI QMLI 'UX.MO.AY 01.13.04.11" -s 500 -t -f internal -o

.. _documentation:

Documentation
~~~~~~~~~~~~~

|Stable Docs|

Full documentation is available at `Read the Docs`_.

Command line documentation is available as help from the command line script:

.. parsed-literal::

   $ |script| --help

Limitations
~~~~~~~~~~~

Note that the correct display of some characters used to represent
components (thin Naval rotors) assumes support for Unicode, while some
aspects of the display of machine state depend on support for combining
Unicode. This is a `known
limitation <https://github.com/orome/crypto-enigma-py/issues/1>`__ that
requres some `console configuration <https://pypi.org/project/win_unicode_console/>`__
changes when used on (some versions) of Windows.

Alternatives
~~~~~~~~~~~~

For other Python Enigma machines see:

-  `py-enigma <https://pypi.python.org/pypi/py-enigma/>`__ (Python 3)

This package is based on a `Haskell version`_, with essentially the same API.


Development status
~~~~~~~~~~~~~~~~~~

|Development Build Status| |Development Docs|

This package is in the early stages of development, and I and can't promise the current
`development version`_ will work. More detail about planned releases and activities
can be found the list of scheduled `milestones`_ and in the list of `open issues`_
and the projects Waffle `status board`_.
Various `test versions`_ may be available for installation or issues review, but these also
may not work as expected.



.. |script| replace:: enigma.py
.. |script_code| replace:: :code:`enigma.py`

.. _machine models: http://www.cryptomuseum.com/crypto/enigma/tree.htm
.. _I: http://www.cryptomuseum.com/crypto/enigma/i/index.htm
.. _M3: http://www.cryptomuseum.com/crypto/enigma/m3/index.htm
.. _M4: http://www.cryptomuseum.com/crypto/enigma/m4/index.htm

.. _development version: https://github.com/orome/crypto-enigma-py/tree/develop
.. _test versions: https://testpypi.python.org/pypi/crypto-enigma
.. _milestones: https://github.com/orome/crypto-enigma-py/milestones
.. _open issues: https://github.com/orome/crypto-enigma-py/issues
.. _status board: https://waffle.io/orome/crypto-enigma-py
.. _Read the Docs: http://crypto-enigma.readthedocs.org/en/pypi/

.. _Enigma machines: http://en.wikipedia.org/wiki/Enigma_machine
.. _Haskell version: https://hackage.haskell.org/package/crypto-enigma
.. _Hackage documentation: https://hackage.haskell.org/package/crypto-enigma/docs/Crypto-Enigma.html

.. |Gitter| image:: https://img.shields.io/gitter/room/badges/shields.svg
   :target: https://gitter.im/orome/crypto-enigma-py
.. |Waffle| image:: https://img.shields.io/waffle/label/orome/crypto-enigma-py/in%20progress.svg?label=active&colorA=66d9ff
   :target: https://waffle.io/orome/crypto-enigma-py
   :alt: 'In Progress Issues'

.. |Python Programming Language| image:: https://img.shields.io/badge/language-Python-blue.svg
   :target: https://www.python.org
.. |PyPi| image:: https://img.shields.io/pypi/v/crypto-enigma.svg
   :target: https://pypi.python.org/pypi/crypto-enigma
.. |Development Docs| image:: https://readthedocs.org/projects/crypto-enigma/badge/?version=latest
   :target: http://crypto-enigma.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status
.. |Stable Docs| image:: https://readthedocs.org/projects/crypto-enigma/badge/?version=pypi
   :target: http://crypto-enigma.readthedocs.org/en/pypi/?badge=pypi
   :alt: Documentation Status
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/crypto-enigma.svg
   :target: https://pypi.python.org/pypi/crypto-enigma/
.. |Development Status| image:: https://img.shields.io/pypi/status/crypto-enigma.svg
   :target: https://pypi.python.org/pypi/crypto-enigma/
.. |BSD3 License| image:: http://img.shields.io/badge/license-BSD3-brightgreen.svg
   :target: https://github.com/orome/crypto-enigma-py/blob/pypi/LICENSE.txt
.. |PyPi Build Status| image:: https://travis-ci.org/orome/crypto-enigma-py.svg?branch=pypi
   :target: https://travis-ci.org/orome/crypto-enigma-py/branches
.. |Development Build Status| image:: https://travis-ci.org/orome/crypto-enigma-py.svg?branch=develop
   :target: https://travis-ci.org/orome/crypto-enigma-py/branches






