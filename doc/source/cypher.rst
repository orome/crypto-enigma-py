.. cypher documentation file

.. warning::

   This documentation under construction and incomplete.

.. note::

    This documentation is in draft form. Reports of any errors or suggestions for improvement are welcomed and
    should be submitted as `new issues`_.

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
