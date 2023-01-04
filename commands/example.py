import main
import argparse


class Command(main.Command):
    name = "example"
    aliases = ["ex"]
    help = "An example command"

    def get_parser(self, subparser: argparse.ArgumentParser):
        subparser.add_argument("--message", type=str,
                            required=True, help="The message to print")
        return subparser

    def run(self, args):
        print(args.message)
