# coding=utf-8

import traceback
import types
import os
import codecs
import re
import imp
import time
import __main__ as main

class PassException( AssertionError ) :
	pass


def ListRemove( lst, value ) :
	try : 
		lst.remove( value )
		return True
	except ValueError :
		return False


g_fixtures = []
g_funcs = []
g_skip = {}

class FuncType :
	Test = 0
	TestCase = 1
	Setup = 2
	Teardown = 3
	FixtureSetup = 4
	FixtureTeardown = 5


class TestEntity :

	def __init__( self, func, type ) :
		self.func = func
		self.type = type

	def GetName( self ) :
		if self.type == FuncType.Test :
			return self.name
		elif self.type == FuncType.TestCase :
			args = map( lambda x: str( x ), self.args ) + map( lambda item : str( item[ 0 ] ) + "=" + str( item[ 1 ] ), self.kvargs.items() )		
			return self.name + "(" + ", ".join( args ) + ")"
		
	def Run( self, fx ) :
		start = time.time()
		try :
			if self.type == FuncType.Test :
				self.func( fx )
			elif self.type == FuncType.TestCase :
				args = ( fx, ) + self.args
				kvargs = self.kvargs
				self.func( *args, **kvargs )
			print "OK (%d ms)" % int( ( time.time() - start ) * 1000.0 )

		except PassException as e :
			print "OK (%d ms)%s" % ( int( ( time.time() - start ) * 1000.0 ), " -" + e.message if e.message else "" ) 

		except Exception as e :
			print e
			print 
			print traceback.format_exc()
			return False

		return True


class Fixture :

	def __init__( self, cls ) :
		self.testclass = cls
		self.name = cls.__name__
		self.tests = []
		for name, method in cls.__dict__.items() :
			if type( method ) == types.FunctionType :
				i = 0
				while i < len( g_funcs ) :
					entity = g_funcs[ i ]
					if entity.func == method :
						if entity.type == FuncType.Test or entity.type == FuncType.TestCase:
							entity.name = name
							self.tests.append( entity )
						elif entity.type == FuncType.Setup :
							self.setup = method
						elif entity.type == FuncType.Teardown :
							self.teardown = method
						elif entity.type == FuncType.FixtureSetup :
							self.fxsetup = method
						elif entity.type == FuncType.FixtureTeardown :
							self.fxteardown = method

						g_funcs.pop( i )
					else :
						i += 1
	
	def RunSetup( self, fx ) :
		try :
			if hasattr( self, "setup" ) :
				self.setup( fx )
			return True
		except Exception as e :
			print "Setup failed"
			print e 
			print
			print traceback.format_exc()
			return False

	def RunTeardown( self, fx ) :
		try :
			if hasattr( self, "teardown" ) :
				self.teardown( fx )
			return True
		except Exception as e :
			print "Teardown failed"
			print e 
			print
			print traceback.format_exc()
			return False

	def RunTests( self ) :
		if self.testclass in g_skip :
			print "%s: Skipped" % self.name
			return

		fx = self.testclass()
		try :
			if hasattr( self, "fxsetup" ) :
				self.fxsetup( fx )

			passed = 0
			skipped = 0
			for test in self.tests :

				print "==================="
				print self.name + "::" + test.GetName()
				if test.func in g_skip :
					print "Skipped"
					skipped += 1
					continue
				
				if self.RunSetup( fx ) and test.Run( fx ) :
					passed += 1
				self.RunTeardown( fx )

			print "\n\n%s: passed %d/%d\n" % ( self.name, passed, len( self.tests ) - skipped )
		
		except Exception as e :
			print "Failed setup for " + self.name
			print e 
			print
			print traceback.format_exc()

		try :
			if hasattr( self, "fxteardown" ) :
				self.fxteardown( fx )

		except Exception as e :
			print "Failed teardown for " + self.name
			print e 
			print
			print traceback.format_exc()


def RunTests() :
	for fx in g_fixtures :
		fx.RunTests()

	for test in g_funcs :
		if test.type != FuncType.Test and test.type != FuncType.TestCase :
			continue

		print "==================="
		print test.func.func_name
		if test.func in g_skip :
			print "Skipped"
			continue

		try :
			start = time.time()
			if test.type == FuncType.Test :
				test.func()
			else :
				test.func( *test.args, **test.kvargs )
			print "OK (%d ms)" % int( ( time.time() - start ) * 1000.0 )

		except PassException as e :
			print "OK (%d ms)%s" % ( int( ( time.time() - start ) * 1000.0 ), " -" + e.message if e.message else "" ) 

		except Exception as e :
			print e
			print 
			print traceback.format_exc()

def RunAllTests() :
	FindTests()
	RunTests()

def FindTests( path=os.getcwd() ) :
	for i in os.listdir( path ) :
		filename = os.path.abspath( os.path.join( path, i ) )
		if os.path.isdir( filename ) :
			FindTests( filename )
		elif filename == main.__file__ :
			continue
		elif "." in filename.rsplit( os.path.sep, 1 )[ 1 ] and i.rsplit( ".", 1 )[ 1 ] == "py" :
			with codecs.open( filename , "r", "utf-8" ) as f :
				code = f.read()

				if re.search( "^@(TestFixture|Test|TestCase\\()\\s", code, re.MULTILINE ) :
					imp.load_source( "", filename )
