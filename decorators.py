from punit import *

def TestFixture( cls ) :
	g_fixtures.append( Fixture( cls ) )
	return cls

def TestMethod( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( RawFunc( method, FuncType.Test ) )
	return method

def Setup( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( RawFunc( method, FuncType.Setup ) )
	return method

def Teardown( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( RawFunc( method, FuncType.Teardown ) )
	return method

def TestFixtureSetup( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( RawFunc( method, FuncType.FixtureSetup ) )
	return method

def TestFixtureTeardown( method ) :
	if method.func_code.co_argcount == 1 :
		g_funcs.append( RawFunc( method, FuncType.FixtureTeardown ) )
	return method