import argparse
import importlib
import inspect
import os
import pkgutil

try:
    import argcomplete
except ImportError:
    argcomplete = None

from . import commands
from . import cmdln
from .commandline import pop_project_package_from_args

debug_mode = True # is overwritten by main.py, for reasons

class Command:
    """
    Base command class which can be extended to create new commands.
    Descriptions and/or helptexts for these commands are taken from the docstring
    of the class and parent class if available.
    """

    name = ""
    aliases = []

    def __init__(self, parent=None):
        self.parent = parent
        self.subparsers = None
        self.commands = {}
        self.command_classes = {}

        if parent:
            self.parser = self.parent.subparsers.add_parser(
                self.name, help=self.get_description(), aliases=self.aliases)
            self.parser.set_defaults(func=self.run, formatter_class=cmdln.HelpFormatter,
                                     usage="%(prog)s [global opts] <command> [--help] [opts] [args]")
        else:
            self.parser = argparse.ArgumentParser(
                prog=self.name, description=self.get_description(), formatter_class=cmdln.HelpFormatter,
                usage="%(prog)s [global opts] <command> [--help] [opts] [args]")
            self.add_parser_arguments()

    def get_description(self):
        result = self.__doc__ or ""
        result = result.strip()
        return result

    @property
    def root_command(self):
        if not self.parent:
            return self
        return self.parent.root_command

    def add_parser_arguments(self):
        raise NotImplementedError()

    def run(self, args):
        raise NotImplementedError()

    def register(self, command_class):
        if not self.subparsers:
            # instantiate subparsers on first use
            self.subparsers = self.parser.add_subparsers(
                dest="command", required=True)

        command = command_class(parent=self)
        command.add_parser_arguments()

        self.commands[command.name] = command

        for alias in getattr(command, "aliases", []):
            self.commands[alias] = command

        return command


class RootCommand(Command):
    MODULES = ()

    def add_parser_arguments(self):
        raise NotImplementedError()

    def run(self, args):
        raise NotImplementedError()

    def load_commands(self):
        for module_prefix, module_path in self.MODULES:
            for loader, module_name, _ in pkgutil.walk_packages(path=[module_path]):
                full_name = f"{module_prefix}.{module_name}"
                spec = loader.find_spec(full_name)
                mod = importlib.util.module_from_spec(spec)
                # TODO: log the failure
                try:
                    spec.loader.exec_module(mod)
                except Exception as e:  # pylint: disable=broad-except
                    if debug_mode: print(f"Failed to load module {full_name}: {e}")
                    continue
                for name in dir(mod):
                    cls = getattr(mod, name)
                    if not inspect.isclass(cls):
                        continue
                    if not issubclass(cls, Command):
                        continue

                    mod_cls_name = f"{module_prefix}.{name}"

                    parent_name = getattr(cls, "parent", None)
                    if parent_name:
                        # allow relative references to classes in the the same module/directory
                        if "." not in parent_name:
                            parent_name = f"{module_prefix}.{parent_name}"

                        # TODO: handle invalid parent name; possibly skip and log
                        parent = self.root_command.command_classes[parent_name]
                        cmd = parent.register(cls)
                    else:
                        cmd = self.root_command.register(cls)

                    self.root_command.command_classes[mod_cls_name] = cmd

    def execute(self, args):
        if debug_mode:
            is_compat_command = "CompatabilityCommand" in str(args.func)
            print(f"CompatabilityCommand={is_compat_command}")
        args.func(args)


class OscMainCommand(RootCommand):
    name = "osc"

    MODULES = (
        ("osc.commands", commands.__path__[0]),
        ("osc.commands.usr_lib", "/usr/lib/osc-plugins"),
        ("osc.commands.usr_local_lib", "/usr/local/lib/osc-plugins"),
        ("osc.commands.var_lib", "/var/lib/osc-plugins"),  # kept for backwards compatibility
        ("osc.commands.home_local_lib", os.path.expanduser("~/.local/lib/osc-plugins")),
        ("osc.commands.home", os.path.expanduser("~/.osc-plugins")),
    )

    def add_parser_arguments(self):
        self.parser.add_argument("-v", "--verbose", action="store_true")
        self.parser.add_argument(
            "-A", "--apiurl",
            metavar="URL",
            help="Open Build Service API URL or a configured alias",
        )

    def run(self, args):
        pass

    def enable_autocomplete(self):
        """
        The method must be called *after* the parser is populated with options and subcommands.
        """
        if not argcomplete:
            return
        argcomplete.autocomplete(self.parser)
