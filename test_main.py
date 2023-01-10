#!/usr/bin/python3

# supposed to be in tests/test_main.py
import unittest
import io
import sys
from main import Command, OscMainCommand


class DummyCommand(Command):
    name = "dummy"
    aliases = ["d"]

    def add_parser_arguments(self):
        pass

    def run(self, args):
        pass


class RepeatCommand(Command):
    """
    Repeat a message a specified number of times
    """

    name = "repeat"
    aliases = ["r"]

    def add_parser_arguments(self):
        pass

    def run(self, args):
        for i in range(args.count):
            print(args.message)


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.command = Command()
        self.main_command = OscMainCommand()

    def test_help_text_shows_up_after_add_parser_arguments(self):
        with self.assertRaises(NotImplementedError):
            self.command.add_parser_arguments()

    def test_command_executes_successfully(self):
        with self.assertRaises(NotImplementedError):
            self.command.run()

    def test_command_is_registered_when_register_is_called(self):
        self.main_command.register(DummyCommand)
        self.assertIn("dummy", self.main_command.commands)
        self.assertIn("d", self.main_command.commands)

    def test_command_is_loaded_from_folder(self):
        self.main_command.load_from_folder('commands')
        self.assertIn("repeat", self.main_command.commands)
        self.assertIn("r", self.main_command.commands)


class TestRepeatCommand(unittest.TestCase):
    def setUp(self):
        self.command = RepeatCommand()

    def test_help_text_shows_up_after_add_parser_arguments(self):
        capture = io.StringIO()
        sys.stdout = capture
        self.command.parser.print_help()
        self.assertIn(
            "Repeat a message a specified number of times", capture.getvalue())
        sys.stdout = sys.__stdout__

    def test_command_executes_successfully(self):
        capture = io.StringIO()
        sys.stdout = capture
        self.command.parser.add_argument("message", type=str,
                                         help="The message to repeat")
        self.command.parser.add_argument("--count", type=int, default=1,
                                         help="The number of times to repeat the message")
        self.command.run(self.command.parser.parse_args(
            ["hello", "--count", "2"]))
        self.assertEqual('hello\nhello\n', capture.getvalue())
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
