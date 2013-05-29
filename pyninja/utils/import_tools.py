
def import_object( module_name, object_name ):
	module = __import__( module_name, globals(), locals(), [object_name] )
	return getattr( module, object_name )