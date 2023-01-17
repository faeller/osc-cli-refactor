import importlib
import os
import pkgutil
from main import Command


def plugin_function_to_command_class(func):
    class PluginCommand(Command):
        _func = func

        def __repr__(self):
            result = super().__repr__()
            result += f"({self._func.__name__})"
            return result

        def get_description(self):
            result = self._func.__doc__ or ""
            result = result.strip()
            return result

        def add_parser_arguments(self):
            options = getattr(self._func, "options", [])
            for option_args, option_kwargs in options:
                self.parser.add_argument(*option_args, **option_kwargs)

        def run(self, *args):
            self._func(args)

    return PluginCommand


class CommandRegistrar:
    def __init__(self, parser):
        self.parser = parser
        self.subparsers = parser.add_subparsers(dest='command', required=True)
        self.commands = {}

    def load_from_folder(self, folder):
        for _, module_name, _ in pkgutil.iter_modules([f"{folder}"]):
            # import module by file path
            folder = os.path.basename(folder)
            module = importlib.import_module(f"{folder}.{module_name}")

            for name, value in module.__dict__.items():
                if callable(value) and name.startswith("do_"):
                    self.register(value)

    def register(self, func):
        command_name = func.__name__[3:]
        command_parser = self.subparsers.add_parser(
            command_name, help=func.__doc__)
        command_parser.set_defaults(func=func)
        self.commands[command_name] = func

    def execute(self, args):
        args.func(args)
