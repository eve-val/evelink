from google.appengine.ext import ndb

from evelink import char, api
from evelink.appengine.api import auto_async

@auto_async
class Char(char.Char):
    __doc__ = char.Char.__doc__

    @ndb.tasklet
    def wallet_balance_async(self):
        api_result = yield self.wallet_info_async()
        raise ndb.Return(
            api.APIResult(
                api_result.result['balance'],
                api_result.timestamp,
                api_result.expires
            )
        )

    @ndb.tasklet
    def event_attendees_async(self, event_id, api_result=None):
        """Returns the attendees for a single event.

        (This is a convenience wrapper around 'calendar_attendees'.)

        NOTE: You must have recently fetched the list of calendar events
        (using the 'calendar_events' method) before calling this method.

        """
        api_result = yield self.calendar_attendees_async([event_id])
        raise ndb.Return(
            api.APIResult(
                api_result.result[int(event_id)],
                api_result.timestamp,
                api_result.expires
            )
        )
