from .. import commandline_new as commandline
from .. import completion


class LsCommand(commandline.Command):
    """
    List sources: projects, packages or files
    """

    name = "ls"

    def add_parser_arguments(self):
        self.parser.add_argument(
            "project",
        ).completer = completion.project

    def run(self, args):
        print(args)
