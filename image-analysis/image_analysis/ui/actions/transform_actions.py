

from traits.api import Bool, Enum, Instance
from traitsui.api import Action, EnumEditor, Handler, Item, OKCancelButtons, View


from image_analysis.commands.transform_commands import FlipCommand


class FlipAction(Action):

    handler = Instance(Handler)

    axis = Enum('horizontal', 'vertical', 'plane', 'time')

    show_dialog = Bool(True)

    def perform(self, event=None):
        command = FlipCommand(data=self.handler.model, axis=self.axis)
        if self.show_dialog:
            image_names = self.handler.names
            ui = command.edit_traits(
                kind='livemodal',
                view=View(
                    Item('axis'),
                    Item('source', editor=EnumEditor(values=image_names)),
                    Item('destination'),
                    buttons=OKCancelButtons,
                )
            )
            if not ui.result:
                return

        self.handler.command_stack.push(command)
