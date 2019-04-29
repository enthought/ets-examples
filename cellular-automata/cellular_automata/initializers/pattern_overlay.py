# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Array, Tuple

from cellular_automata.abstract_initializer import AbstractInitializer


class PatternOverlay(AbstractInitializer):
    """ Overlay a pattern at a specified position. """

    #: The pattern to overlay.
    pattern = Array(dtype='uint8')

    #: The place to put the pattern.  If a value is -1 then place at center.
    position = Tuple((-1, -1))

    def initialize_states(self, states):
        position = [x if x != -1 else n//2
                    for x, n in zip(self.position, states.shape)]
        slices = [slice(x-n//2, x-n//2+n)
                  for x, n in zip(position, self.pattern.shape)]
        states[tuple(slices)] = self.pattern
        return states
