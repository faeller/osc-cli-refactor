from .. import commandline_new as commandline


class OriginCommand(commandline.Command):
    name = "origin"

    def add_parser_arguments(self):
        pass

    def run(self, args):
        pass

    def register(self, command_class):
        super().register(command_class)
