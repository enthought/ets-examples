Cellular Automata
=================

This is a collection of packages that allow simulation of cellular automata
such as Conway's Game of Life or elementary 1D rules, such as Rule 30.

Installation
------------

You can create an appropriate environment with the following
`EDM commands <http://docs.enthought.com/edm/>`_::

    edm install -e cellular-automata chaco scipy pyqt
    edm run -e cellular-automata pip install .

and you can switch into that environment with::

    edm shell -e cellular-automata

If you prefer to use ``pip``, you can install into an existing environment
with::

    pip install .[pyqt]

Usage
-----

Design Notes
------------

License
-------

This software is provided without warranty under the terms of the BSD
license included in LICENSE.txt and may be redistributed only
under the conditions described in the aforementioned license.  The license
is also available online at http://www.enthought.com/licenses/BSD.txt
