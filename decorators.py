# coding=utf-8
import types
from punit import *

def TestFixture( cls ) :
	if type( cls ) == types.ClassType :
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
		te.skip = "skip" in kvargs and kvargs[ "skip" ]
		te.repeat = "repeat" in kvargs and kvargs[ "repeat" ]

		if "skip" in kvargs :
			del kvargs[ "skip" ]
		if "repeat" in kvargs :
			del kvargs[ "repeat" ]
		te.kvargs = kvargs
		g_funcs.append( te )
		return method

	return wrapper

def Skip( methodOrClass ) :
	g_skip[ methodOrClass ] = True
	return methodOrClass