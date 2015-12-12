.. components documentation file

.. warning::

   This documentation under construction and incomplete.

.. note::

    This documentation is in draft form. Reports of any errors or suggestions for improvement are welcomed and
    should be submitted as `new issues`_.

********************************************
Components - :mod:`crypto_enigma.components`
********************************************

.. automodule:: crypto_enigma.components

Overview
========

.. autosummary::
    :nosignatures:

      Component
      ~Component.name
      ~Component.wiring
      ~Component.turnovers
      ~Component.mapping
      ~Direction
      ~crypto_enigma.components.component
      ~crypto_enigma.components.rotors
      ~crypto_enigma.components.reflectors

Machine components
==================

.. autoclass:: Component

.. autosimple:: Component.__init__

Component properties
====================

.. autoattribute:: Component.name
.. autoattribute:: Component.wiring
.. autoattribute:: Component.turnovers

The component mapping
=====================

.. automethod:: Component.mapping

.. autoclass:: Direction

.. _component_getting:

Getting components
==================

.. autofunction:: crypto_enigma.components.component

.. autodata:: crypto_enigma.components.rotors
    :annotation:

.. autodata:: crypto_enigma.components.reflectors
    :annotation:
