
from ..NinjaDevice import NinjaDevice

class TemperatureNinjaDevice(NinjaDevice):
	@property
	def current_temperature( self ):
		return self._get_data( 'last_data', {} ).get( 'DA', None )
	
	def get_default_reading( self ):
		return ('Temperature', '%.1f C' % self.current_temperature)