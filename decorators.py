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
		f = TestEntity( method, FuncType.TestCase )
		f.args = args
		f.kvargs = kvargs
		g_funcs.append( f )
		return method

	return wrapper

def Skip( methodOrClass ) :
	g_skip[ methodOrClass ] = True
	return methodOrClass