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

Enigma machine configurations and their functionality are represented using single class:

.. autoclass:: EnigmaConfig()

.. _config_creation:

Creating configurations
=======================

.. automethod:: EnigmaConfig.config_enigma
.. automethod:: EnigmaConfig.config_enigma_from_string

.. _config_state:

State
=====

The behavior of an Enigma machine, for both its :ref:`operation <config_operation>` and
the :ref:`encodings <config_encoding>` it performs is determined entirely by its state.
This state is established when a machine is set to its initial configuration. Operation
then produces a series of configurations each with new state

Formally, that state consists of :ref:`internal <config_state_internal>` elements not directly
visible to the operator who can only indirectly :ref:`see changes <config_state_visible>` in the
positions of the rotors as manifest in the rotor letters at the machine windows.

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

All encoding functionality is built upon a single class:

.. autoclass:: Mapping()
    :show-inheritance:

.. autosimple:: Mapping.__init__

.. todo::

    Correct use of a term/definition for this, and a variable to link back consistently.

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


