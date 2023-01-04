from main import Command


class Command(Command):
    name = "repeat"
    aliases = ["r"]
    help = "Repeat a message a specified number of times"

    def get_parser(self, subparser):
        subparser.add_argument("message", type=str,
                               help="The message to repeat")
        subparser.add_argument("--count", type=int, default=1,
                               help="The number of times to repeat the message")
        return subparser

    def run(self, args):
        for i in range(args.count):
            print(args.message)
