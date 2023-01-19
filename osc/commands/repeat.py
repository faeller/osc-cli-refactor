from .. import commandline


class RepeatCommand(commandline.Command):
    """
    Repeat a message a specified number of times
    """

    name = "repeat"
    aliases = ["r"]

    def add_parser_arguments(self):
        self.parser.add_argument("message", type=str,
                               help="The message to repeat")
        self.parser.add_argument("--count", type=int, default=1,
                               help="The number of times to repeat the message")

    def run(self, args):
        for i in range(args.count):
            print(args.message)
