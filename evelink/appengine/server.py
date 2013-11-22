from google.appengine.ext import ndb

from evelink import server
from evelink.appengine.api import auto_gae_api


class Server(server.Server):
    """Wrapper around /server/ of the EVE API for Google App Engine.

    Implement async methods

    """

    @auto_gae_api
    def __init__(self, api=None):
        self.api = api

    @ndb.tasklet
    def server_status_async(self):
        api_result = yield self.api.get_async('server/ServerStatus')
        raise ndb.Return(self.server_status(api_result=api_result))
