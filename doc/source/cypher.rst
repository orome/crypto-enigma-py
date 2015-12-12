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

Overview
========

.. autosummary::
    :nosignatures:

      Mapping
      ~Mapping.encode_string
      ~Mapping.encode_char

Substitution cypher mappings
============================

All encoding functionality is built upon a single class:

.. autoclass:: Mapping()
    :show-inheritance:

.. _mapping_encoding:

Mapping encoding
================

.. autosimple:: Mapping.__init__

For reference, two functions are provided to perform a mappings substitution cypher, though
these will rarely be used directly:

.. automethod:: Mapping.encode_string
.. automethod:: Mapping.encode_char

