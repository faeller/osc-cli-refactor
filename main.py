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


def main():
    # Create the main parser
    parser = argparse.ArgumentParser(prog="osc")
    parser.add_argument("command", type=str, help="The command to run")
    args, unknown_args = parser.parse_known_args()

    # Get the command module and class
    command_module = None
    command_class = None
    for _, module_name, _ in pkgutil.iter_modules(["commands"]):
        if module_name == args.command:
            command_module = importlib.import_module(f"commands.{module_name}")
            command_class = getattr(command_module, "Command")
            break

    if not command_module or not command_class:
        print(f"Unknown command: {args.command}")
        return

    # Create the command instance
    command = command_class()

    # Parse the command-specific arguments using the command's parser
    command_parser = command.get_parser()
    command_args = command_parser.parse_args(unknown_args)

    # Run the command
    command.run(command_args)


if __name__ == "__main__":
    main()
