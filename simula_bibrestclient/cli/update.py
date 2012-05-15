from simula_bibrestclient.client import BibFolder
from simula_bibrestclient.mime import mimetypes
from .argparseimport import FileType
from .main import Command


class Update(Command):
    #: Name of the command.
    name = 'update'

    #: Help for the command.
    help = 'Update bibliography items from a local file on the formats returned by the "search" command.'

    @classmethod
    def setup_args(cls, parser):
        parser.add_argument('--mimetype', default='application/json',
                           choices=mimetypes,
                           help="Mimetype for the output. Defaults to application/json.")
        parser.add_argument('filename', type=FileType('r'),
                            help=('The file containing data to upload to the '
                                  'server. The format is the same as the one '
                                  'returned by "search" with the same '
                                  '--mimetype.'))

    def __init__(self, args, auth):
        folder = BibFolder(folderurl=args.folderurl, decode_output=False,
                           mimetype=args.mimetype, **auth)
        data = args.filename.read()
        try:
            response = folder.put(data)
        except Exception, e:
            print e
        else:
            print response
