=========================
Cellular Automata Library
=========================

.. image:: images/cellular-automata.gif
   :height: 435

This example shows how to build a library using Traits for the object models.
The key design patterns are:

* use of :py:class:`ABCHasStrictTraits` to specify interfaces and basic
  implementation and subclasses to provide particular implementations.  In
  particular look at :py:class:`.AbstractRule` and the various classes defined
  in :py:mod:`cellular_automata.rules` to see this pattern in action.

* use of traits listeners to handle collecting the history and statistics of
  a simulation, rather than writing particular classes to handle this.  In
  particular look at the interaction between :py:class:`.AutomataRecorder` and
  :py:class:`.CellularAutomaton`.

* use of composition of behaviours to extend capabilties, rather than
  subclassing.  For example, rather than having a separate class for each type
  of cellular automaton, behaviours are factored out into separate rule classes
  with simple behaviour and the cellular automaton gets a list of rules that
  in aggregate define its behaviour.  This allows significant increased
  flexibility, including the ability to change the rules dynamically (eg.
  a game of life automata can be changed mid-run to a forest fire simulation
  if desired).  This is particularly powerful when combined with a GUI.

Cellular Automata Library Documentation
=======================================

.. py:module:: cellular_automata

Module ``cellular_automata.cellular_automaton``
-----------------------------------------------

.. automodule:: cellular_automata.cellular_automaton
    :members:

Module ``cellular_automata.abstract_initializer``
-------------------------------------------------

.. automodule:: cellular_automata.abstract_initializer
    :members:

Module ``cellular_automata.abstract_rule``
------------------------------------------

.. automodule:: cellular_automata.abstract_rule
    :members:

Module ``cellular_automata.automata_recorder``
----------------------------------------------

.. automodule:: cellular_automata.automata_recorder
    :members:

Module ``cellular_automata.automata_traits``
--------------------------------------------

.. automodule:: cellular_automata.automata_traits
    :members:

Module ``cellular_automata.initializers.constant``
--------------------------------------------------

.. automodule:: cellular_automata.initializers.constant
    :members:

Module ``cellular_automata.initializers.pattern_overlay``
---------------------------------------------------------

.. automodule:: cellular_automata.initializers.pattern_overlay
    :members:

Module ``cellular_automata.initializers.random_choice``
-------------------------------------------------------

.. automodule:: cellular_automata.initializers.random_choice
    :members:

Module ``cellular_automata.rules.base_rules``
---------------------------------------------

.. automodule:: cellular_automata.rules.base_rules
    :members:

Module ``cellular_automata.rules.binary_morphology``
----------------------------------------------------

.. automodule:: cellular_automata.rules.binary_morphology
    :members:

Module ``cellular_automata.rules.change_state_rule``
----------------------------------------------------

.. automodule:: cellular_automata.rules.change_state_rule
    :members:

Module ``cellular_automata.rules.elementary_1d_rule``
-----------------------------------------------------

.. automodule:: cellular_automata.rules.elementary_1d_rule
    :members:

Module ``cellular_automata.rules.forest``
-----------------------------------------

.. automodule:: cellular_automata.rules.forest
    :members:

Module ``cellular_automata.rules.life``
---------------------------------------

.. automodule:: cellular_automata.rules.life
    :members:

Module ``cellular_automata.io.image``
-------------------------------------

.. automodule:: cellular_automata.io.image
    :members:

Module ``cellular_automata.io.text``
------------------------------------

.. automodule:: cellular_automata.io.text
    :members:
