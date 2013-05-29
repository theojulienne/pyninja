"""PyNinja CLI.

Usage:
  pyninja user info
  pyninja device list
  pyninja device info <guid>
  pyninja device actuate <guid> <value>
  pyninja (-h | --help)

Options:
  -h --help     Show this screen.

"""
from docopt import docopt

from clint.textui import puts, indent, colored

from pyninja import NinjaAPI, NinjaException

class NinjaCLI(object):
	def main( self, arguments ):
		# set up the ninja API creds
		# FIXME: this should eventually support a real config file of some sort
		# as well as automagically creating the file etc.
		self.api = NinjaAPI.with_user_token_file( '~/ninja_token.txt' )
		
		# call the actual function that does the work
		main_functions = [ ('user', 'info'), ('device', 'list'), ('device', 'info'), ('device', 'actuate') ]
		for names in main_functions:
			func = '_'.join( names )
			if all( [arguments[name] for name in names] ):
				try:
					getattr(self, '_cmd_' + func)( arguments )
				except NinjaException as e:
					puts( colored.red( 'Error: ' + e.message ) )
	
	def _cmd_user_info( self, arguments ):
		user = self.api.user
		
		puts()
		puts( colored.green( 'User Info' ) )
		with indent( 2 ):
			for item in ('id', 'name', 'email', 'pusherChannel'):
				self._show_info( item, user[item] )
		puts()
	
	def _cmd_device_list( self, arguments ):
		device_list = self.api.devices
		
		puts()
		puts( colored.green( 'Devices (%d)' % len(device_list) ) )
		puts()
		with indent( 2 ):
			for device in device_list:
				self._show_device_info( device )
				
				puts( )
	
	def _cmd_device_info( self, arguments ):
		guid = arguments['<guid>']
		
		device = self.api.get_device( guid )
		
		self._show_device_info( device )
	
	def _cmd_device_actuate( self, arguments ):
		guid = arguments['<guid>']
		value = arguments['<value>']
		
		device = self.api.get_device( guid )
		
		try:
			device.actuate( value )
		except ValueError as e:
			puts( colored.red( 'Invalid value: ' + e.message ) )
			return
		
		self._show_device_info( device )
		puts( )
		self._show_info( 'New Value', value )
	
	def _show_device_info( self, device ):
		self._show_info( 'GUID', device.guid )
		self._show_info( 'Name', device.default_name )
		self._show_info( 'Type', device.__class__.__name__ )
		
		# show the device's default sensor reading, if available
		sensed = device.get_default_reading( )
		if sensed is not None:
			name, value = sensed
			self._show_info( name, value )
	
	def _show_info( self, name, value ):
		puts( colored.cyan(name + ': ') + value )

def main():
	arguments = docopt( __doc__, version='PyNinja CLI 0.1' )
	
	cli = NinjaCLI( )
	cli.main( arguments )