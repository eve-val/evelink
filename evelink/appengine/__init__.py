try:
	from evelink.appengine.api import AppEngineAPI
	from evelink.appengine.api import AppEngineCache
	from evelink.appengine.api import AppEngineDatastoreCache
	from evelink.appengine import server
	from evelink.appengine import eve

	__all__ = [
	  "AppEngineAPI",
	  "AppEngineCache",
	  "AppEngineDatastoreCache",
	  "server",
	  "eve",
	]
	
except ImportError:
	pass
