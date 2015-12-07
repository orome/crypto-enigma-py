.. cypher documentation file

.. warning::

   This documentation under construction and incomplete.

.. note::

   Full documentation for the API currently under construction (here). In the meantime the `Hackage documentation`_
   for the `Haskell version`_ (which has essentially the same API) serves as a temporary substitute.

************************************
Cypher - :mod:`crypto_enigma.cypher`
************************************

.. automodule:: crypto_enigma.cypher

Substitution cypher mappings
============================

All encoding functionality is built upon a single class:

.. autoclass:: Mapping()
    :show-inheritance:

.. _mapping_encoding:

Mapping encoding
================

.. autosimple:: Mapping.__init__

.. automethod:: Mapping.encode_string
.. automethod:: Mapping.encode_char

.. todo::

    Correct use of a term/definition for this, and a variable to link back consistently.
