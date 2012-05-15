from simula_bibrestclient.client import BibFolder
from simula_bibrestclient.mime import mimetypes
from .main import Command


class Search(Command):
    #: Name of the command.
    name = 'search'

    #: Help for the command.
    help = 'Search for bibliographies.'

    @classmethod
    def setup_args(cls, parser):
        parser.add_argument('--mimetype', default='application/json',
                           choices=mimetypes,
                           help="Mimetype for the output. Defaults to application/json.")
        parser.add_argument('--simula_author_username', action='append',
                            help=('Simula author username. May be repeated to '
                                  'match multiple users. Gets all publications '
                                  'where the specified simula user(s) is among '
                                  'the authors. Example: "hpl".'))
        parser.add_argument('--mine', action='store_true',
                            help='Add your own username to --simula_author_username.')
        parser.add_argument('--author_name', action='append',
                            help=('Author name. May be repeated to match '
                                  'multiple authors. Gets all publications where '
                                  'the specified name is among the authors. '
                                  'Example: "Langtangen H"'))
        parser.add_argument('--search',
                            help='Search for text within the publication. Matches text within most attributes (I.e.: You can search for one or more words within title, abstract, ...).')
        parser.add_argument('--itemid',
                            help=('Bibliography item id. May be repeated to match bibliography items.'
                                  'Example: "Simula.simula.1212".'))

    def __init__(self, args, auth):
        folder = BibFolder(folderurl=args.folderurl, decode_output=False,
                           mimetype=args.mimetype, **auth)
        simula_author_usernames = args.simula_author_username or []
        if args.mine:
            simula_author_usernames.append(auth['username'])

        paramcount = 0
        for param in (simula_author_usernames, args.author_name, args.search, args.itemid):
            if param:
                paramcount += 1
            if paramcount > 1:
                raise SystemExit('Supplying more than one of (--simula_author_username/--mine), --author_name, --search or --itemid makes no sense, since only the first one is used in the liste order.')

        response = folder.search(simula_author_usernames=simula_author_usernames,
                                 author_names=args.author_name,
                                 search=args.search,
                                 itemids=args.itemid)
        print response
