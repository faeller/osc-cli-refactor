from .. import commandline_new as commandline
from .. import completion
from ..core import get_osc_version


class VersionCommand(commandline.Command):
    #     """
    #     Give version of osc binary

    #     usage:
    #         osc version
    #     """

    name = "version"

    def add_parser_arguments(self):
        self.parser.completer = completion.project

    def run(self, args):
        print(get_osc_version())
