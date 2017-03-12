import types
from punit import *

def TestFixture( cls ) :
	if isinstance( cls, type ) :
		g_fixtures.append( Fixture( cls ) )
	return cls

def Test( method ) :
	if type( method ) == types.FunctionType or type( method ) == types.MethodType :
		g_funcs.append( TestEntity( method, FuncType.Test ) )
	return method

def Setup( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( TestEntity( method, FuncType.Setup ) )
	return method

def Teardown( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( TestEntity( method, FuncType.Teardown ) )
	return method

def TestFixtureSetup( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( TestEntity( method, FuncType.FixtureSetup ) )
	return method

def TestFixtureTeardown( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( TestEntity( method, FuncType.FixtureTeardown ) )
	return method

def TestCase( *args, **kvargs ) :
	def wrapper( method ) :
		if type( method ) != types.FunctionType and type( method ) != types.MethodType :
			return method

		te = TestEntity( method, FuncType.TestCase )
		te.args = args

		if "skip" in kvargs :
			g_skip[ method ] = True
			del kvargs[ "skip" ]
		if "repeat" in kvargs :
			te.repeat = kvargs[ "repeat" ]
			del kvargs[ "repeat" ]
		if "description" in kvargs :
			te.description = kvargs[ "description" ]
			del kvargs[ "description" ]
		if "result" in kvargs :
			te.result = kvargs[ "result" ]
			del kvargs[ "result" ]
		if "exception" in kvargs :
			te.exception = kvargs[ "exception" ]
			del kvargs[ "exception" ]
		if "exceptionPattern" in kvargs :
			te.exceptionPattern = kvargs[ "exceptionPattern" ]
			del kvargs[ "exceptionPattern" ]

		te.kvargs = kvargs
		g_funcs.append( te )
		return method

	return wrapper

def Skip( methodOrClass ) :
	g_skip[ methodOrClass ] = True
	return methodOrClass