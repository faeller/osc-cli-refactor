import argparse

from .. import commandline_new as commandline


class ExampleCommand(commandline.Command):
    """
    An example command
    """

    name = "example"
    aliases = ["ex"]

    def add_parser_arguments(self):
        self.parser.add_argument("--message", type=str,
                            required=True, help="The message to print")

    def run(self, args):
        print(args.message)
