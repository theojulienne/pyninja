from setuptools import setup, find_packages

setup(
	name = 'pyninja',
	version = '0.1',
	description = '',
	author = 'Theo Julienne',
	url = 'https://github.com/theojulienne/pyninja',
	license = 'MIT',
	packages = find_packages('.'),
	entry_points = {
		'console_scripts': [
			'pyninja = pyninja.cli.NinjaCLI:main',
		]
	},
	install_requires=[
		'docopt',
		'clint',
		'requests',
		'pygments',
		'clint',
		'webcolors',
	]
)
