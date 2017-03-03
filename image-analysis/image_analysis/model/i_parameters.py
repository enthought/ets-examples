

from traits.api import Interface


class IParameters(Interface):
    """ A set of parameters for an operation. """

    def to_function_args(self):
        """ Convert the parameters to positional and keyword arguments.

        Returns
        -------
        args : tuple
            The positional arguments of the parameters.
        kwargs : dict
            The keyword arguments of the parameters.
        """
        raise NotImplementedError()
