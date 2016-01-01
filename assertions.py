def Assert( value, message ) :
	if not value :
		raise AssertionError( message )

def IsTrue( value ) :
	Assert( value, "Expected True" )

def IsFalse( value ) :
	Assert( not value, "Expected False" )

def AreEquals( expected, actual ) :
	Assert( expected == actual, "Expected " + str( expected ) + ", but was " + str( actual ) )