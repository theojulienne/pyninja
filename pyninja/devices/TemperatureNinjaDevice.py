
from ..NinjaDevice import NinjaDevice

class TemperatureNinjaDevice(NinjaDevice):
	@property
	def current_temperature( self ):
		data = self._get_data( 'last_data', {} ).get( 'DA', None )
		if not isinstance(data, float) and not isinstance(data, int):
			return None
		return data
	
	def get_default_reading( self ):
		temp = self.current_temperature
		if temp is None:
			return ('Temperature', 'Unknown')
		else:
			return ('Temperature', '%.1f C' % temp)