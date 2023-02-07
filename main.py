#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK


import os

import osc.commandline_new as commandline
import osc.commandline_compat_layer as compatibility_layer


def main():
    compatibility_layer.test()
    main_command = commandline.OscMainCommand()
    topdir = os.path.dirname(__file__)
    main_command.load_commands()
    
    for legacy_command in compatibility_layer.get_all_compat_wrapped_commands():
        if not legacy_command.name in main_command.commands:
            main_command.register(legacy_command)

    main_command.enable_autocomplete()
    args = main_command.parser.parse_args()
    main_command.execute(args)


if __name__ == "__main__":
    main()
