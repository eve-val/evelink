from google.appengine.ext import ndb

from evelink import server
from evelink.appengine.api import auto_gae_api


class Server(server.Server):
    __doc__ = server.Server.__doc__

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api

    @ndb.tasklet
    def server_status_async(self):
        """Asynchronous version of server_status."""
        api_result = yield self.api.get_async('server/ServerStatus')
        raise ndb.Return(self.server_status(api_result=api_result))
