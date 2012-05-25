class Command(object):
    """
    Base class for simula_bibrestclient subcommands.
    """
    #: Name of the command. Must be defined in subclasses.
    name = None

    #: Help for the command. Must be defined in subclasses.
    help = None

    requires_auth = True

    @classmethod
    def setup_args(cls, parser):
        """
        Add commands to the parser for this subcommand.

        :param parser: An :class:`argparse.ArgumentParser` object.
        """
        parser.add_argument('--mimetype')

    @classmethod
    def execute(cls, args, auth):
        cls(args, auth)
