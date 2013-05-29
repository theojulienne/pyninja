from .NinjaObject import NinjaObject

from .utils.import_tools import import_object

class NinjaDevice(NinjaObject):
	_device_type_map = {
		'rgbled': 'RGBLEDNinjaDevice',
		'temperature': 'TemperatureNinjaDevice',
		'humidity': 'HumidityNinjaDevice',
	}
	
	@classmethod
	def from_api_response( cls, api, response ):
		target_cls = cls
		if 'device_type' in response and response['device_type'] in cls._device_type_map:
			device_class_name = cls._device_type_map[response['device_type']]
			target_cls = import_object( 'pyninja.devices.' + device_class_name, device_class_name )
		return target_cls( api, response )
	
	def actuate( self, value ):
		result = self._api._call_api( 'device/%s' % self.guid, data={ 'DA': value }, http_method='put' )
		return ( result.get( 'result', 0 ) == 1 )
	
	def get_default_reading( self ):
		return None
	
	@property
	def last_value( self ):
		return self._get_data( 'last_data', {} ).get( 'DA', None )