from main import Command
import argparse


class Command(Command):
    name = "repeat"
    aliases = ["r"]
    help = "Repeat a message a specified number of times"

    def get_parser(self):
        parser = argparse.ArgumentParser(prog=self.name, description=self.help)
        parser.add_argument("message", type=str, help="The message to repeat")
        parser.add_argument("--count", type=int, default=1,
                            help="The number of times to repeat the message")
        return parser

    def run(self, args):
        for i in range(args.count):
            print(args.message)
