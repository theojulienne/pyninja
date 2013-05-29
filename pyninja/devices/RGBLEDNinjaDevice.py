import re
from webcolors import name_to_hex, rgb_to_hex

from ..NinjaDevice import NinjaDevice

NINJA_COLOR_RE = r'^[0-9A-Fa-f]{6}$'

class RGBLEDNinjaDevice(NinjaDevice):
	@property
	def current_color( self ):
		return self.last_value
	
	def actuate( self, color ):
		if isinstance(color, tuple) and len(color) == 3:
			color = rgb_to_hex( color )
		
		if isinstance(color, basestring):
			# check if the color is already in ninja-api supported format
			# if not, we'll pass it through webcolors
			if not re.match( NINJA_COLOR_RE, color ):
				if not color.startswith( '#' ):
					color = name_to_hex( color )
				
				# ninja-api compatible color spec
				color = color.lstrip( '#' ).upper()
			
			return super(RGBLEDNinjaDevice, self).actuate( color )
		else:
			raise ValueError( 'Color value must be a valid css3 color name or an (r,g,b) tuple' )
	
	def set_color( self, color ):
		return self.actuate( color )
	
	def get_default_reading( self ):
		return ('Color', '#%s' % self.current_color)