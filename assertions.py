# coding=utf-8

import math
from punit import PassException

def IsTrue( value ) :
	assert value, "Expected True"

def IsFalse( value ) :
	assert not value, "Expected False"

def IsNone( value ) :
	assert value == None, "Expected " + str( value ) + " is None"

def IsNotNone( value ) :
	assert value == None, "Expected " + str( value ) + " is not None"

def IsNan( value ) :
	assert type( value ) == float, "Expected float, but was " + str( type( value ) )
	assert math.isnan( value ), "Expected NaN, but was " + str( value )

def IsNotNan( value ) :
	assert type( value ) == float, "Expected float, but was " + str( type( value ) )
	assert not math.isnan( value ), "Expected not NaN"

def IsEmpty( value ) :
	assert type( value ) == string or type( value ) == list or type( value ) == dict
	assert not value, "Expected empty, but was " + str( value )

def IsNotEmpty( value ) :
	assert type( value ) == string or type( value ) == list or type( value ) == dict
	assert value, "Expected not empty value"

def AreEqual( expected, actual ) :
	assert expected == actual, "Expected " + str( expected ) + ", but was " + str( actual )

def AreNotEqual( expected, actual ) :
	assert expected != actual, "Expected not " + str( expected ) + ", but was " + str( actual )

def AreSame( expected, actual ) :
	assert expected is actual, "Expected " + str( expected ) + " is the same that " + str( actual )

def AreNotSame( expected, actual ) :
	assert expected is not actual, "Expected " + str( expected ) + " is not the same that " + str( actual )

def Greater( v1, v2 ) :
	assert v1 > v2, "Expected " + str( v1 ) + " > " + str( v2 )

def GreaterOrEqual( v1, v2 ) :
	assert v1 > v2, "Expected " + str( v1 ) + " >= " + str( v2 )

def Less( v1, v2 ) :
	assert v1 < v2, "Expected " + str( v1 ) + " < " + str( v2 )

def LessOrEqual( v1, v2 ) :
	assert v1 < v2, "Expected " + str( v1 ) + " <= " + str( v2 )

def Throws( exceptionType, func, *args, **kvargs ) :
	try :
		func( *args, **kvargs )
	except Exception as e :
		assert type( e ) == exceptionType, "Expected exception of type " + str( exceptionType ) + ", but was " + str( type( e ) )
	else :
		raise AssertionError( "Expected exception of type " + str( exceptionType ) )

def Catch( exceptionType, func, *args, **kvargs ) :
	try :
		func( *args, **kvargs )
	except Exception as e :
		assert isinstance( e, exceptionType ), "Expected exception of type " + str( exceptionType ) + " or derived, but was " + str( type( e ) )
	else :
		raise AssertionError( "Expected exception of type " + str( exceptionType ) + " or derived" )

def Pass( message=None ) :
	raise PassException( message )

def Fail( message=None ) :
	raise AssertionError( message )