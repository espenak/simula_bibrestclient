import sys

from simula_bibrestclient import defaults
from .argparseimport import ArgumentParser
from .command import Command
from .search import Search
from .update import Update
from .version import Version


_subcommands = []
def _register_command(commandcls):
    """
    Register a :class:`simula_bibrestclient.cli.command.Command` subclass
    as a simula_bibrestclient command.
    """
    if not issubclass(commandcls, Command):
        raise TypeError('Must be a Command subclass.')
    if commandcls in _subcommands:
        raise ValueError('{0} is already in the commands registry.'.format(commandcls))
    _subcommands.append(commandcls)

_register_command(Search)
_register_command(Update)
_register_command(Version)



def _add_subcommand(subparsers, cls):
    parser = subparsers.add_parser(cls.name, help=cls.help)
    parser.set_defaults(func=cls.execute, requires_auth=cls.requires_auth)
    cls.setup_args(parser)


def main(arguments=None, subcommands=[]):
    """
    The simula_bibrestclient command.

    :param arguments:
        Command-line arguments as a list, excluding the program name.
        Defaults to ``sys.args[1:]``.
    :param subcommands:
        List of :class:`.Command`-subclasses.
    """
    from getpass import getuser, getpass

    arguments = arguments or sys.argv[1:]
    subcommands = subcommands or _subcommands
    parser = ArgumentParser(description='Simula publication database REST API command line client.')
    parser.add_argument('-u', '--username', default=getuser(),
                        help='Username on the Simula website. Defaults to the current user ({0}).'.format(getuser()))
    parser.add_argument('--folderurl', default=defaults.folderurl, dest='folderurl',
                        help=('Override the bibliography folder URL. For '
                              'debugging or usage against the testserver. '
                              'Defaults to: {0}').format(defaults.folderurl))
    subparsers = parser.add_subparsers(title='Subcommands',
                                       description='The following subcommands are available. Use "{prog} <action> --help" for help with a specific command.'.format(prog=parser.prog),
                                       help='sub-command help')
    for subcommand in subcommands:
        _add_subcommand(subparsers, subcommand)

    args = parser.parse_args(arguments)
    if args.requires_auth:
        auth = dict(username=args.username,
                    password=getpass('Password on the Simula website for {0}: '.format(args.username)))
    else:
        auth = None
    args.func(args, auth)
