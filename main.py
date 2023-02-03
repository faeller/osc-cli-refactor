#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK


import os

import osc.commandline_new as commandline


def main():
    main_command = commandline.OscMainCommand()
    topdir = os.path.dirname(__file__)
    main_command.load_commands()
    main_command.enable_autocomplete()
    args = main_command.parser.parse_args()
    main_command.execute(args)


if __name__ == "__main__":
    main()
