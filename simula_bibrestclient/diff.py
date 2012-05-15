"""
Helpers for generating a diff of two python objects.
"""

from difflib import ndiff
from pprint import pformat

def _prettyformatlist(pydata):
    string = pformat(pydata)
    return string.splitlines(True)

def create_diff(pydataA, pydataB):
    """
    Return a string containing the diff of ``pydataA`` and ``pydataB``.
    """
    diff = ndiff(_prettyformatlist(pydataA), _prettyformatlist(pydataB))
    return ''.join(diff)

def create_stringdiff(stringA, stringB):
    """
    Return a string containing the diff of ``stringA`` and ``stringB``.
    """
    diff = ndiff(stringA, stringB)
    return ''.join(diff)
