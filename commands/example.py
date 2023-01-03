import main
import argparse


class Command(main.Command):
    name = "example"
    aliases = ["ex"]
    help = "An example command"

    def get_parser(self):
        parser = argparse.ArgumentParser(prog=self.name, description=self.help)
        parser.add_argument("--message", type=str,
                            required=True, help="The message to print")
        return parser

    def run(self, args):
        print(args.message)
