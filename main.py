#!/usr/bin/python3


import argparse
import importlib
import os
import pkgutil


class Command:
    """
    This program does this and that...
    """

    name = ""
    aliases = []

    def __init__(self, parent=None):
        self.parent = parent
        if parent:
            self.parser = self.parent.subparsers.add_parser(self.name, help=self.get_description(), aliases=self.aliases)
        else:
            self.parser = argparse.ArgumentParser(prog=self.name, description=self.get_description())
        self.subparsers = None
        self.commands = {}

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
            self.subparsers = self.parser.add_subparsers(dest="command", required=True)

        command = command_class(parent=self)
        command.add_parser_arguments()

        self.commands[command.name] = command

        for alias in command.aliases:
            self.commands[alias] = command

    def load_from_folder(self, folder):
        for _, module_name, _ in pkgutil.iter_modules([f"{folder}"]):
            # XXX: dirty hack; import module by file path
            folder = os.path.basename(folder)
            module = importlib.import_module(f"{folder}.{module_name}")

            if hasattr(module, "Command"):
                command_class = getattr(module, "Command")
                self.register(command_class)

    def execute(self, args):
        command = self.commands[args.command]
        command.run(args)


class OscMainCommand(Command):
    name = "osc"


def main():
    main_command = OscMainCommand()
    topdir = os.path.dirname(__file__)
    main_command.load_from_folder(os.path.join(topdir, "commands"))
    args = main_command.parser.parse_args()
    main_command.execute(args)


if __name__ == "__main__":
    main()
