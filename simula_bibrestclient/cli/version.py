from simula_bibrestclient import version
from .main import Command


class Version(Command):
    #: Name of the command.
    name = 'version'

    #: Help for the command.
    help = 'Show current version of simula_bibrestclient.'

    requires_auth = False

    @classmethod
    def setup_args(cls, parser):
        pass

    def __init__(self, args, auth):
        print version
