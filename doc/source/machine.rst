.. machine documentation file

.. warning::

   This documentation under construction and incomplete.

.. note::

   Full documentation for the API currently under construction (here). In the meantime the `Hackage documentation`_
   for the `Haskell version`_ (which has essentially the same API) serves as a temporary substitute.

**************************************
Machine - :mod:`crypto_enigma.machine`
**************************************

.. automodule:: crypto_enigma.machine

Machine configurations
======================

.. autoclass:: EnigmaConfig()

.. _config_creation:

Creating configurations
=======================

.. automethod:: EnigmaConfig.config_enigma
.. automethod:: EnigmaConfig.config_enigma_from_string

.. _config_state:

State
=====

.. _config_state_visible:

Visible state
-------------

.. automethod:: EnigmaConfig.windows

.. _config_state_internal:

Internal state
--------------

.. autosimple:: EnigmaConfig.__init__

.. autoattribute:: EnigmaConfig.components
.. autoattribute:: EnigmaConfig.positions
.. autoattribute:: EnigmaConfig.rings

.. _config_operation:

State transitions and operation
===============================

.. automethod:: EnigmaConfig.step
.. automethod:: EnigmaConfig.stepped_configs

.. automethod:: EnigmaConfig.print_operation

.. _config_encoding:

Encoding
========

.. _config_encoding_message:

Message encoding
----------------

.. automethod:: EnigmaConfig.enigma_encoding
.. automethod:: EnigmaConfig.print_encoding
.. automethod:: EnigmaConfig.make_message

.. _config_encoding_mappings:

Mappings
--------

.. automethod:: EnigmaConfig.stage_mapping_list
.. automethod:: EnigmaConfig.enigma_mapping_list
.. automethod:: EnigmaConfig.enigma_mapping

Exceptions
==========

.. autoexception:: EnigmaError
    :show-inheritance:

.. autoexception:: EnigmaValueError
    :show-inheritance:

.. autoexception:: EnigmaDisplayError
    :show-inheritance:


