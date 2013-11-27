from evelink import corp
from evelink.appengine.api import auto_async


@auto_async
class Corp(corp.Corp):
    __doc__ = corp.Corp.__doc__
