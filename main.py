import argparse
import importlib
import pkgutil


class Command:
    name = ""
    aliases = []
    help = ""

    def get_parser(self):
        raise NotImplementedError("get_parser method not implemented")

    def run(self, *args):
        raise NotImplementedError("run method not implemented")


class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, command):
        self.commands[command.name] = command

        for alias in command.aliases:
            self.commands[alias] = command

    def get(self, name):
        return self.commands.get(name)

    def setup_subparsers(self, parser):
        subparsers = parser.add_subparsers(dest="command", required=True)

        for command in set(self.commands.values()):
            print("setting up subparser for", command.name)
            subparser = subparsers.add_parser(
                command.name, help=command.help, aliases=command.aliases)
            command.get_parser(subparser)

    def load_from_folder(self, folder, main_parser=None):
        for _, module_name, _ in pkgutil.iter_modules([f"{folder}"]):
            module = importlib.import_module(f"{folder}.{module_name}")

            if hasattr(module, "Command"):
                command_class = getattr(module, "Command")
                self.register(command_class())

        if(main_parser):
            self.setup_subparsers(main_parser)

    def execute(self, name, args):
        command = self.get(name)
        if not command:
            print(f"Unknown command: {name}")
            return

        command.run(args)


def main():
    command_registry = CommandRegistry()

    # Create the main parser
    parser = argparse.ArgumentParser(prog="osc")

    command_registry.load_from_folder("commands", parser)
    print(command_registry.commands.keys())

    args = parser.parse_args()
    command_registry.execute(args.command, args)


if __name__ == "__main__":
    main()
