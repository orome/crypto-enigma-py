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

.. todo::

    Move this to a new `Mapping` class, with an encode method?

The Enigma machine, and the components from which it is constructed, use **mappings** to perform a
`simple substitution encoding`_.
Mappings describe the cryptographic effects of each component's fixed `~.components.Component.wiring`;
the encoding they perform individually in a machine based on their rotational `~EnigmaConfig.positions` and
the direction in which a singnal passes through them (see `~.components.Component.mapping`);
and, the progressive (`~EnigmaConfig.stage_mapping_list`) and
overall (`~EnigmaConfig.enigma_mapping_list`
and `~EnigmaConfig.enigma_mapping`) encoding performed by the machine as a whole.

Mappings are  expressed as a string of letters indicating the mapped-to letter
for the letter at that position in the alphabet — i.e., as a permutation of the alphabet.
For example, the mapping **EKMFLGDQVZNTOWYHXUSPAIBRCJ** encodes **A** to **E**, **B** to **K**, **C** to **M**, ...,
**Y** to **C**, and **Z** to **J**.

.. todo::

    Explain mappings here and link to this. Correct use of a term/definition for this, and a variable to link back.

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


