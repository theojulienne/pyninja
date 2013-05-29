import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

class NinjaObject(object):
	@classmethod
	def from_api_response( cls, api, response ):
		return cls( api, response )
	
	def __init__( self, api, data ):
		self._api = api
		self._data = data
	
	def __getattr__( self, name ):
		if name in self._data:
			return self._data[name]
		else:
			raise AttributeError, '%s has no attribute \'%s\'' % (self.__class__.__name__, name)
	
	def __getitem__( self, name ):
		return self._data[name]
	
	def _get_data( self, name, default=None ):
		return self._data.get( name, default )
	
	def print_debug( self ):
		json_repr = json.dumps( self._data, indent=4 )
		print( highlight( json_repr, JsonLexer(), TerminalFormatter() ) )