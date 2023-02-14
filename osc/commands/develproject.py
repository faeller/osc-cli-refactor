from .. import commandline_new as commandline
from .. import completion
import sys
from ..core import show_devel_project
from _private import api


class DevelprojectCommand(commandline.Command):
    """
    Print the devel project / package of a package

    Examples:
        osc develproject [PROJECT PACKAGE]
    """

    name = "develproject"
    aliases = ["bsdevelproject", "dp"]

    def add_parser_arguments(self):
        self.parser.add_argument(
            "project",
        ).completer = completion.project
        pass

    def run(self, args):
        apiurl = api.get_api_url()

        project, package = commandline.pop_project_package_from_args(
            args.positional_args, default_project=".", default_package=".")

        devel_project, devel_package = show_devel_project(apiurl, project, package)

        if not devel_project:
            print(f"Package {project}/{package} has no devel project", file=sys.stderr)
            sys.exit(1)

        print(f"{devel_project}/{devel_package}")
