try:
	from evelink.appengine.api import AppEngineAPI
	from evelink.appengine.api import AppEngineCache
	from evelink.appengine.api import AppEngineDatastoreCache
	from evelink.appengine import server

	__all__ = [
	  "AppEngineAPI",
	  "AppEngineCache",
	  "AppEngineDatastoreCache",
	  "server"
	]
	
except ImportError:
	pass