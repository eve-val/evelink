from evelink import account
from evelink.appengine.api import auto_async

@auto_async
class Account(account.Account):
    __doc__ = account.Account.__doc__

    def __init__(self, api):
        self.api = api
