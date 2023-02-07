from osc.commandline_new import Command
from osc.commandline import Osc
import inspect


def call_osc_babysitter_if_compat_failed():
    pass


def convert_osc_do_function_to_command_class(func):
    class CompatabilityWrappedCommand(Command):
        _func = func
        name = _func.__name__[3:]
        aliases = getattr(_func, "aliases", [])

        def __repr__(self):
            result = super().__repr__()
            result += f"({self._func.__name__})"
            return result

        def get_description(self):
            result = self._func.__doc__ or ""
            result = result.strip()
            return result

        def add_parser_arguments(self):
            options = getattr(self._func, "options", [])
            for option_args, option_kwargs in options:
                self.parser.add_argument(*option_args, **option_kwargs)

        def run(self, *args):
            options = getattr(self._func, "options", [])
            self._func(args, options)

    return CompatabilityWrappedCommand


def get_all_compat_wrapped_commands():
    commands = []
    for name in dir(Osc):
        if not name.startswith("do_"):
            continue

        func = getattr(Osc, name)

        if not inspect.isfunction(func):
            continue

        commands.append(convert_osc_do_function_to_command_class(func))
    return commands


def test():
    # print(get_all_compat_wrapped_commands())
    pass
