# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import HasStrictTraits


class AbstractInitializer(HasStrictTraits):
    """ Abstract base class for states intializers. """

    def initialize(self, states):
        """ Modify the provided states to their initial state.

        Default implementation does nothing.

        Parameters
        ----------
        states : array
            The initial array of states to be modified.

        Returns
        -------
        states : array
            The states after having been modified by the initializer.
        """
        return states
