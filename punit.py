import traceback
import types
import os
import codecs
import re
import imp
import time
import __main__ as main

import assertions

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
g_totalSkipped = 0
g_totalPassed = 0
g_totalRunned = 0

class FuncType :
	Test = 0
	TestCase = 1
	Setup = 2
	Teardown = 3
	FixtureSetup = 4
	FixtureTeardown = 5


class TestEntity( object ) :

	def __init__( self, func, type ) :
		self.name = func.__name__
		self.func = func
		self.type = type
		self.repeat = 1
		self.description = ""
		self.result = None
		self.exception = None
		self.exceptionPattern = None

	def GetName( self ) :
		name = self.name
		if self.type == FuncType.TestCase :
			args =  [ str( x ) if type( x ) != str else ( "'" + str( x ) + "'" ) for x in self.args ]
			args += [ str( item[ 0 ] ) + "=" + str( item[ 1 ] ) for item in self.kvargs.items() ]
			name += "(" + ", ".join( args ) + ")"
		if self.description :
			name += " -- " + self.description
		return name
		
	def Run( self, fx ) :
		start = time.time()
		global g_totalRunned
		g_totalRunned += 1
		try :
			for i in range( self.repeat ) :
				if fx :
					if self.type == FuncType.Test :
						self.func( fx )
					elif self.type == FuncType.TestCase :
						args = ( fx, ) + self.args
						kvargs = self.kvargs
						result = self.func( *args, **kvargs )
				else :
					if self.type == FuncType.Test :
						self.func()
					else :
						result = self.func( *self.args, **self.kvargs )

				if self.result :
					assertions.AreEqual( self.result, result )

			if self.exception :
				raise AssertionError( "Expected exception of type " + self.exception.__name__ )
			
			print( "OK ({0} ms)".format( int( ( time.time() - start ) * 1000.0 ) ) )

		except PassException as e :
			print( "OK ({0} ms)%s".format( int( ( time.time() - start ) * 1000.0 ), " - " + e.args[ 0 ] if e.args[ 0 ] else "" ) )

		except BaseException as e :
			if self.exception and isinstance( e, self.exception ) :
				if self.exceptionPattern and not re.match( self.exceptionPattern, e.args[ 0 ] ) :
					print( str( e ) + " ({0} ms)".format( int( ( time.time() - start ) * 1000.0 ) ) )
					print()
					print( traceback.format_exc() )
					return False
				else :
					print( "OK ({0} ms)".format( int( ( time.time() - start ) * 1000.0 ) ) )
			else :
				print( str( e ) + " ({0} ms)".format( int( ( time.time() - start ) * 1000.0 ) ) )
				print()
				print( traceback.format_exc() )
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
			print( "Setup failed" )
			print( e )
			print()
			print( traceback.format_exc() )
			return False

	def RunTeardown( self, fx ) :
		try :
			if hasattr( self, "teardown" ) :
				self.teardown( fx )
			return True
		except Exception as e :
			print( "Teardown failed" )
			print( e )
			print()
			print( traceback.format_exc() )
			return False

	def RunTests( self, forceRunSkipped=False ) :
		global g_totalSkipped
		global g_totalPassed

		if self.testclass in g_skip and not forceRunSkipped :
			print( self.name + ": Skipped" )
			g_totalSkipped += len( self.tests )
			return

		fx = self.testclass()
		try :
			if hasattr( self, "fxsetup" ) :
				self.fxsetup( fx )

			passed = 0
			skipped = 0
			for test in self.tests :

				print( "===================" )
				print( self.name + "::" + test.GetName() )
				if test.func in g_skip and not forceRunSkipped :
					print( "Skipped" )
					skipped += 1
					g_totalSkipped += 1
					continue
				
				if self.RunSetup( fx ) and test.Run( fx ) :
					passed += 1
					g_totalPassed += 1
				self.RunTeardown( fx )

			print( "\n\n{0}: passed {1}/{2} ({3} skipped)\n".format( self.name, passed, len( self.tests ) - skipped, skipped ) )
		
		except Exception as e :
			print( "Failed setup for " + self.name )
			print( e )
			print()
			print( traceback.format_exc() )

		try :
			if hasattr( self, "fxteardown" ) :
				self.fxteardown( fx )

		except Exception as e :
			print( "Failed teardown for " + self.name )
			print( e )
			print()
			print( traceback.format_exc() )


def RunTests( forceRunSkipped=False ) :
	global g_totalSkipped
	global g_totalPassed
	global g_totalRunned

	g_totalSkipped = 0
	g_totalPassed = 0
	g_totalRunned = 0

	for fx in g_fixtures :
		fx.RunTests( forceRunSkipped )

	testsByFiles = {}
	for test in g_funcs :
		file = os.path.relpath( test.func.__code__.co_filename )
		if file not in testsByFiles :
			testsByFiles[ file ] = []
		testsByFiles[ file ].append( test )

	for file, tests in testsByFiles.items() :
		passed = 0
		skipped = 0
		for test in tests :
			if test.type != FuncType.Test and test.type != FuncType.TestCase :
				continue

			print( "===================" )
			print( test.GetName() )
			if test.func in g_skip and not forceRunSkipped :
				print( "Skipped" )
				skipped += 1
				g_totalSkipped += 1
				continue

			if test.Run( None ) :
				passed += 1
				g_totalPassed += 1

		print( "\n\n{0}: passed {1}/{2} ({3} skipped)\n".format( file, passed, len( tests ) - skipped, skipped ) )

	print( "Total: passed {0}/{1} ({2} skipped)\n".format( g_totalPassed, g_totalRunned, g_totalSkipped ) )


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
		elif "." in filename.rsplit( os.path.sep, 1 )[ 1 ] and i.rsplit( ".", 1 )[ 1 ] in [ "py", "pyw" ] :
			with open( filename , "r", encoding="utf-8" ) as f :
				code = f.read()

				if re.search( r"^@(TestFixture|Test|TestCase\()\s", code, re.MULTILINE ) :
					imp.load_source( "", filename )
