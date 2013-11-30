from google.appengine.ext import ndb

from evelink import corp
from evelink.appengine.api import auto_async


@auto_async
class Corp(corp.Corp):
    __doc__ = corp.Corp.__doc__

    @ndb.tasklet
    def members_async(self, extended=True):
        """Returns details about each member of the corporation."""
        args = {}
        if extended:
            args['extended'] = 1
        
        api_result = yield self.api.get_async(
        	'corp/MemberTracking', params=args
        )
        raise ndb.Return(
        	self.members(extended=extended, api_result=api_result)
        )