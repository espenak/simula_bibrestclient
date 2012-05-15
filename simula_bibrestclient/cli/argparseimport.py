try:
    from argparse import *
except ImportError:
    # Python 2.6
    from .argparse_for_oldpython import *
