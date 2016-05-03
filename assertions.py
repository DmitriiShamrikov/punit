# coding=utf-8
import math

def IsTrue( value ) :
	assert value, u"Expected True"

def IsFalse( value ) :
	assert not value, u"Expected False"

def IsNone( value ) :
	assert value == None, u"Expected " + unicode( value ) + u" is None"

def IsNotNone( value ) :
	assert value != None, u"Expected " + unicode( value ) + u" is not None"

def IsNan( value ) :
	assert type( value ) == float, u"Expected float, but was " + unicode( type( value ) )
	assert math.isnan( value ), u"Expected NaN, but was " + unicode( value )

def IsNotNan( value ) :
	assert type( value ) == float, u"Expected float, but was " + unicode( type( value ) )
	assert not math.isnan( value ), u"Expected not NaN"

def IsEmpty( value ) :
	assert isinstance( value, basestring ) or isinstance( value, list ) or isinstance( value, dict )
	assert not value, u"Expected empty, but was " + unicode( value )

def IsNotEmpty( value ) :
	assert isinstance( value, basestring ) or isinstance( value, list ) or isinstance( value, dict )
	assert value, u"Expected not empty value"

def AreEqual( expected, actual ) :
	assert expected == actual, u"Expected " + unicode( expected ) + u", but was " + unicode( actual )

def AreNotEqual( expected, actual ) :
	assert expected != actual, u"Expected not " + unicode( expected ) + u", but was " + unicode( actual )

def AreSame( expected, actual ) :
	assert expected is actual, u"Expected " + unicode( expected ) + u" is the same that " + unicode( actual )

def AreNotSame( expected, actual ) :
	assert expected is not actual, u"Expected " + unicode( expected ) + u" is not the same that " + unicode( actual )

def Greater( v1, v2 ) :
	assert v1 > v2, u"Expected " + unicode( v1 ) + u" > " + unicode( v2 )

def GreaterOrEqual( v1, v2 ) :
	assert v1 > v2, u"Expected " + unicode( v1 ) + u" >= " + unicode( v2 )

def Less( v1, v2 ) :
	assert v1 < v2, u"Expected " + unicode( v1 ) + u" < " + unicode( v2 )

def LessOrEqual( v1, v2 ) :
	assert v1 < v2, u"Expected " + unicode( v1 ) + u" <= " + unicode( v2 )

def Throws( exceptionType, func, *args, **kvargs ) :
	try :
		func( *args, **kvargs )
	except Exception as e :
		assert type( e ) == exceptionType, "Expected exception of type " + exceptionType.__name__ + ", but was " + type( e ).__name__
	else :
		raise AssertionError( "Expected exception of type " + exceptionType.__name__ )

def Catch( exceptionType, func, *args, **kvargs ) :
	try :
		func( *args, **kvargs )
	except Exception as e :
		assert isinstance( e, exceptionType ), "Expected exception of type " + exceptionType.__name__ + " or derived, but was " + type( e ).__name__
	else :
		raise AssertionError( "Expected exception of type " + exceptionType.__name__ + " or derived" )

def Pass( message=None ) :
	raise PassException( message )

def Fail( message=None ) :
	raise AssertionError( message )