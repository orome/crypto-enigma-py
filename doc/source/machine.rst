.. machine documentation file

.. warning::

   This documentation under construction and incomplete.

.. note::

    This documentation is in draft form. Reports of any errors or suggestions for improvement are welcomed and
    should be submitted as `new issues`_.

**************************************
Machine - :mod:`crypto_enigma.machine`
**************************************

.. automodule:: crypto_enigma.machine

Machine configurations
======================

Enigma machine configurations and their functionality are represented using single class:

.. autoclass:: EnigmaConfig()

.. autosummary::
    :nosignatures:

      ~EnigmaConfig.config_enigma
      ~EnigmaConfig.config_enigma_from_string
      ~EnigmaConfig.windows
      ~EnigmaConfig.components
      ~EnigmaConfig.positions
      ~EnigmaConfig.rings
      ~EnigmaConfig.stage_mapping_list
      ~EnigmaConfig.enigma_mapping_list
      ~EnigmaConfig.enigma_mapping
      ~EnigmaConfig.step
      ~EnigmaConfig.stepped_configs
      ~EnigmaConfig.print_operation
      ~EnigmaConfig.enigma_encoding
      ~EnigmaConfig.print_encoding

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
positions of the rotors as manifest in the rotor letters at the machine windows. This internal
state is entirely responsible for determining the :ref:`mappings used by the machine <config_state_mappings>` to
encode messages.

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

.. _config_state_mappings:

Mappings
--------

The Enigma machine's state determines the |mappings| it uses to perform :ref:`encodings <config_encoding>`.
Thes mappings can be examined in a number of ways:

.. automethod:: EnigmaConfig.stage_mapping_list
.. automethod:: EnigmaConfig.enigma_mapping_list
.. automethod:: EnigmaConfig.enigma_mapping

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

Exceptions
==========

.. autoexception:: EnigmaError
    :show-inheritance:

.. autoexception:: EnigmaValueError
    :show-inheritance:

.. autoexception:: EnigmaDisplayError
    :show-inheritance:


