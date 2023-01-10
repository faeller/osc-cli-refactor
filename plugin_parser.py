import importlib
import os
import pkgutil

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
        command_parser = self.subparsers.add_parser(command_name, help=func.__doc__)
        command_parser.set_defaults(func=func)
        self.commands[command_name] = func

    def execute(self, args):
        args.func(args)