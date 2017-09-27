
from traits.api import HasStrictTraits, provides


from .i_parameters import IParameters


@provides(IParameters)
class BaseParameters(HasStrictTraits):

    def to_function_args(self):
        """ Convert the parameters to positional and keyword arguments.

        By default this constructs keyword arguments out of all traits where
        the 'parameter' metadata is True.

        Returns
        -------
        args : tuple
            The positional arguments of the parameters, always empty for
            default.
        kwargs : dict
            The keyword arguments of the parameters.
        """
        kwargs = {name: getattr(self, name)
                  for name in self.trait_names(parameter=True)}
        return (), kwargs
