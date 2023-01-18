#!/usr/bin/python3


import os

import osc.commandline


def main():
    main_command = osc.commandline.OscMainCommand()
    topdir = os.path.dirname(__file__)
    main_command.load_from_folder(os.path.join(topdir, "osc", "commands"), "osc.commands.")
    args = main_command.parser.parse_args()
    main_command.execute(args)


if __name__ == "__main__":
    main()
