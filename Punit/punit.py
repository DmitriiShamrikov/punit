# coding=utf-8

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


class TestEntity :

	def __init__( self, func, type ) :
		self.name = func.func_name
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
			args = map( lambda x: unicode( x ) if type( x ) != str and type( x ) != unicode else ( "'" + unicode( x ) + "'" ), self.args ) \
				 + map( lambda item : unicode( item[ 0 ] ) + u"=" + unicode( item[ 1 ] ), self.kvargs.items() )
			name += u"(" + u", ".join( args ) + u")"
		if self.description :
			name += u" -- " + self.description
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
			
			print u"OK (%d ms)" % int( ( time.time() - start ) * 1000.0 )

		except PassException as e :
			print u"OK (%d ms)%s" % ( int( ( time.time() - start ) * 1000.0 ), u" - " + e.message if e.message else u"" )

		except self.exception as e :
			if self.exceptionPattern and not re.match( self.exceptionPattern, e.message ) :
				print unicode( e ) + u" (%d ms)" % int( ( time.time() - start ) * 1000.0 )
				print 
				print traceback.format_exc()
				return False
			else :
				print u"OK (%d ms)" % int( ( time.time() - start ) * 1000.0 )

		except Exception as e :
			print unicode( e ) + u" (%d ms)" % int( ( time.time() - start ) * 1000.0 )
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
			print u"Setup failed"
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
			print u"Teardown failed"
			print e 
			print
			print traceback.format_exc()
			return False

	def RunTests( self ) :
		global g_totalSkipped
		global g_totalPassed

		if self.testclass in g_skip :
			print u"%s: Skipped" % self.name
			g_totalSkipped += len( self.tests )
			return

		fx = self.testclass()
		try :
			if hasattr( self, "fxsetup" ) :
				self.fxsetup( fx )

			passed = 0
			skipped = 0
			for test in self.tests :

				print u"==================="
				print self.name + "::" + test.GetName()
				if test.func in g_skip :
					print u"Skipped"
					skipped += 1
					g_totalSkipped += 1
					continue
				
				if self.RunSetup( fx ) and test.Run( fx ) :
					passed += 1
					g_totalPassed += 1
				self.RunTeardown( fx )

			print u"\n\n%s: passed %d/%d (%d skipped)\n" % ( self.name, passed, len( self.tests ) - skipped, skipped )
		
		except Exception as e :
			print u"Failed setup for " + self.name
			print e 
			print
			print traceback.format_exc()

		try :
			if hasattr( self, "fxteardown" ) :
				self.fxteardown( fx )

		except Exception as e :
			print u"Failed teardown for " + self.name
			print e 
			print
			print traceback.format_exc()


def RunTests() :
	global g_totalSkipped
	global g_totalPassed
	global g_totalRunned

	g_totalSkipped = 0
	g_totalPassed = 0
	g_totalRunned = 0

	for fx in g_fixtures :
		fx.RunTests()

	testsByFiles = {}
	for test in g_funcs :
		file = os.path.relpath( test.func.func_code.co_filename )
		if file not in testsByFiles :
			testsByFiles[ file ] = []
		testsByFiles[ file ].append( test )

	for file, tests in testsByFiles.items() :
		passed = 0
		skipped = 0
		for test in tests :
			if test.type != FuncType.Test and test.type != FuncType.TestCase :
				continue

			print u"==================="
			print test.GetName()
			if test.func in g_skip :
				print u"Skipped"
				skipped += 1
				g_totalSkipped += 1
				continue

			if test.Run( None ) :
				passed += 1
				g_totalPassed += 1

		print u"\n\n%s: passed %d/%d (%d skipped)\n" % ( file, passed, len( tests ) - skipped, skipped )

	print "Total: passed %d/%d (%d skipped)\n" % ( g_totalPassed, g_totalRunned, g_totalSkipped )


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
			with codecs.open( filename , "r", "utf-8" ) as f :
				code = f.read()

				if re.search( "^@(TestFixture|Test|TestCase\\()\\s", code, re.MULTILINE ) :
					imp.load_source( "", filename )
