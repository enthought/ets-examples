

from apptools.undo.api import AbstractCommand
from traits.api import Dict, Enum, Str, Trait


class DataCommand(AbstractCommand):

    _data_before = Dict

    _data_after = Dict

    def do(self):
        self._data_before = self.data.get_data()
        self._do(self)
        self._data_after = self.data.get_data()

    def undo(self):
        self.data.set_data(self._data_before)

    def redo(self):
        self.data.set_data(self._data_after)

    def _do(self):
        raise NotImplementedError()
