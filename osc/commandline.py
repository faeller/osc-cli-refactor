import argparse
import importlib
import pkgutil


class Command:
    """
    Base command which can be extended to create new commands.
    Descriptions and/or helptexts for these commands are taken from the docstring of the class and parent class if available.
    """

    name = ""
    aliases = []

    def __init__(self, parent=None):
        self.parent = parent
        self.subparsers = None
        self.commands = {}

        if parent:
            self.parser = self.parent.subparsers.add_parser(
                self.name, help=self.get_description(), aliases=self.aliases)
        else:
            self.parser = argparse.ArgumentParser(
                prog=self.name, description=self.get_description())

    def get_description(self):
        result = self.__doc__ or ""
        result = result.strip()
        return result

    def add_parser_arguments(self):
        raise NotImplementedError()

    def run(self, *args):
        raise NotImplementedError()

    def register(self, command_class):
        if not self.subparsers:
            # instantiate subparsers on first use
            self.subparsers = self.parser.add_subparsers(
                dest="command", required=True)

        command = command_class(parent=self)
        command.add_parser_arguments()

        self.commands[command.name] = command

        for alias in command.aliases:
            self.commands[alias] = command

    def load_from_folder(self, folder, module_prefix):
        for _, module_name, _ in pkgutil.iter_modules([f"{folder}"]):
            # XXX: dirty hack; import module by file path
            #folder = os.path.basename(folder)
            module = importlib.import_module(f"{module_prefix}{module_name}")

            if hasattr(module, "Command"):
                command_class = getattr(module, "Command")
                self.register(command_class)

    def execute(self, args):
        command = self.commands[args.command]
        command.run(args)


class OscMainCommand(Command):
    name = "osc"
