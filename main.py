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

    def register_all(self):
        for _, module_name, _ in pkgutil.iter_modules(["commands"]):
            module = importlib.import_module(f"commands.{module_name}")
            command_class = getattr(module, "Command")
            self.register(command_class())

    def execute(self, name, args):
        command = self.get(name)
        if not command:
            print(f"Unknown command: {name}")
            return

        parser = command.get_parser()
        command_args = parser.parse_args(args)
        command.run(command_args)


commands = CommandRegistry()


def main():
    # Create the main parser
    parser = argparse.ArgumentParser(prog="osc")
    parser.add_argument("command", type=str, help="The command to run")

    commands.register_all()

    args, unknown_args = parser.parse_known_args()
    # execute
    commands.execute(args.command, unknown_args)


if __name__ == "__main__":
    main()
