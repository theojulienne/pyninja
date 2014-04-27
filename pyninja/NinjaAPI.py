import requests
import os

from .NinjaException import NinjaException
from .NinjaUser import NinjaUser
from .NinjaDevice import NinjaDevice

class NinjaAPI(object):
	@classmethod
	def with_user_token_file( cls, token_file ):
		token = open(os.path.expanduser(token_file)).read().strip()
		return cls( user_access_token=token )
	
	def __init__( self, user_access_token=None, api_server=None ):
		self._user_access_token = user_access_token
		if api_server is None:
		    api_server = os.environ.get( 'NINJA_API_HOST', 'https://api.ninja.is/' )
		self._api_server = api_server
	
	def _call_api( self, endpoint, data=None, unwrap_data=False, http_method='get' ):
		params = {
			'user_access_token': self._user_access_token
		}
		
		http_call = getattr( requests, http_method )
		response = http_call( self._api_server + 'rest/v0/%s' % endpoint, params=params, data=data )
		
		if response.status_code != 200:
			raise NinjaException( 'API returned HTTP response code %d' % response.status_code )
		
		json = response.json
		
		if callable(json):
			json = json()
		
		if json is None:
			raise NinjaException( 'API returned empty response (are you authenticated?)' )
		
		if unwrap_data:
			if json['result'] != 1 or json['error'] is not None:
				raise NinjaException( 'API responded with error: %s' % json['error'] )

			data = json['data']

			return data
		else:
			return json
	
	def _bind_object( self, klass, *args, **kwargs ):
		data = self._call_api( *args, **kwargs )
		return klass.from_api_response( self, data )
	
	def _bind_objects( self, klass, *args, **kwargs ):
		for data in self._call_api( *args, **kwargs ):
			yield klass.from_api_response( self, data )
	
	@property
	def device_dict( self ):
		devices = {}
		for guid,data in self._call_api( 'devices', unwrap_data=True ).iteritems():
			data['guid'] = guid
			devices[guid] = NinjaDevice.from_api_response( self, data )
		return devices
	
	@property
	def devices( self ):
		return self.device_dict.values()

	@property
	def user( self ):
		return self._bind_object( NinjaUser, 'user' )
	
	def get_device( self, guid ):
		return self._bind_object( NinjaDevice, 'device/%s' % guid, unwrap_data=True )