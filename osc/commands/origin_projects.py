from .. import commandline


class OriginProjectsCommand(commandline.Command):
    """
    An example command
    """

    name = "projects"
    aliases = ["p"]
    parent = "osc.commands.OriginCommand"

    def add_parser_arguments(self):
        self.parser.add_argument("--message", type=str,
                                 required=True, help="The message to print")

    def run(self, args):
        print(args.message)
