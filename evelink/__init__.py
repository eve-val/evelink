"""EVELink - Python bindings for the EVE API."""

import logging

from evelink import account
from evelink import api
from evelink import char
from evelink import constants
from evelink import corp
from evelink import eve
from evelink import map
from evelink import server

__version__ = "0.7.5"

# Implement NullHandler because it was only added in Python 2.7+.
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# Create a logger, but by default, have it do nothing
_log = logging.getLogger('evelink')
_log.addHandler(NullHandler())

# Update the version number used in the user-agent
api._user_agent = 'evelink v%s' % __version__

__all__ = [
  "account",
  "api",
  "char",
  "constants",
  "corp",
  "eve",
  "map",
  "parsing",
  "server",
]
