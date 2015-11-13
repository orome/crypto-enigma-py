crypto-enigma
-------------

|Python Programming Language| |PyPi| |Supported Python versions| |Development Status| |BSD3 License| |PyPi Build Status|

An Enigma machine simulator with state and encoding display for Python 2.7.

Currently support is only provided for those `machine models`_ in most
widespread general use during the war years: the `I`_, `M3`_, and `M4`_.

Functionality
~~~~~~~~~~~~~

Encode messages:

.. code-block:: sh

    $ python enigma.py encode "B-I-III-I EMO UX.MO.AY 13.04.11" "TESTINGXTESTINGUD"
    OZQKPFLPYZRPYTFVU

    $ python enigma.py encode "B-I-III-I EMO UX.MO.AY 13.04.11" "OZQKPFLPYZRPYTFVU"
    TESTINGXTESTINGUD

Show configuration details:

.. code-block:: sh

    $ python enigma.py show "B-I-III-I EMO UX.MO.AY 13.04.11" -l 'X' -H'()' -f internal
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

Simulate machine operation:

.. code-block:: sh

    $ python enigma.py run "B-I-III-I EMO UX.MO.AY 13.04.11" -m "TESTING" -t -H'()'
    0000       CNAUJVQSLEMIKBZRGPHXDFYTWO   EMO  19 10 05
    0001  T > UNXKGVERLYDIQBTWMHZ(O)AFPCJS  EMP  19 10 06
    0002  E > QTYJ(Z)XUPKDIMLSWHAVNBGROFCE  EMQ  19 10 07
    0003  S > DMXAPTRWKYINBLUESG(Q)FOZHCJV  ENR  19 11 08
    0004  T > IUSMHRPEAQTVDYWGJFC(K)BLOZNX  ENS  19 11 09
    0005  I > WMVXQRLS(P)YOGBTKIEFHNZCADJU  ENT  19 11 10
    0006  N > WKIQXNRSCVBOY(F)LUDGHZPJAEMT  ENU  19 11 11
    0007  G > RVPTWS(L)KYXHGNMQCOAFDZBEJIU  ENV  19 11 12

Documentation
~~~~~~~~~~~~~

Command line documentation is available as help from the command line script:

.. code-block:: sh

   $ python enigma.py --help

Full documentation for the API is not yet available, but the `Hackage documentation`_ for the
`Haskell version`_ (which has essentially the same API) serves as a temporary substitute.

Limitations
~~~~~~~~~~~

Note that the correct display of some characters used to represent
components (thin Naval rotors) assumes support for Unicode, while some
aspects of the display of machine state depend on support for combining
Unicode. This is a `known
limitation <https://github.com/orome/crypto-enigma-py/issues/1>`__ that
will be addressed in a future release.

Alternatives
~~~~~~~~~~~~

For other Python Enigma machines see:

-  `py-enigma <https://pypi.python.org/pypi/py-enigma/>`__ (Python 3)


Development status
~~~~~~~~~~~~~~~~~~

|Development Build Status|

This package is in the early stages of development, and I and can't promise the
`development version`_ will work. More detail about planned releases and activities
can be found the list of scheduled `milestones`_ and in the list of `open issues`_.


.. _machine models: http://www.cryptomuseum.com/crypto/enigma/tree.htm
.. _I: http://www.cryptomuseum.com/crypto/enigma/i/index.htm
.. _M3: http://www.cryptomuseum.com/crypto/enigma/m3/index.htm
.. _M4: http://www.cryptomuseum.com/crypto/enigma/m4/index.htm

.. _development version: https://github.com/orome/crypto-enigma-py/tree/develop
.. _milestones: https://github.com/orome/crypto-enigma-py/milestones
.. _open issues: https://github.com/orome/crypto-enigma-py/issues

.. _Enigma machines: http://en.wikipedia.org/wiki/Enigma_machine
.. _Haskell version: https://hackage.haskell.org/package/crypto-enigma
.. _Hackage documentation: https://hackage.haskell.org/package/crypto-enigma/docs/Crypto-Enigma.html

.. |Python Programming Language| image:: https://img.shields.io/badge/language-Python-blue.svg
   :target: https://www.python.org
.. |PyPi| image:: https://img.shields.io/pypi/v/crypto-enigma.svg
   :target: https://pypi.python.org/pypi/crypto-enigma
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



