
from ..NinjaDevice import NinjaDevice

class HumidityNinjaDevice(NinjaDevice):
	@property
	def current_humidity( self ):
		return self._get_data( 'last_data', {} ).get( 'DA', None )
	
	def get_default_reading( self ):
		return ('Humidity', '%.1f %%' % self.current_humidity)