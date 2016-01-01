import traceback
import types

def ListRemove( lst, value ) :
	try : 
		lst.remove( value )
		return True
	except ValueError :
		return False


g_fixtures = []
g_funcs = []

class FuncType :
	Test = 0
	TestCase = 1
	Setup = 2
	Teardown = 3
	FixtureSetup = 4
	FixtureTeardown = 5

class RawFunc :

	def __init__( self, func, type ) :
		self.func = func
		self.type = type


class TestEntity :

	def __init__( self, name, func ) :
		self.name = name
		self.func = func

	def GetName( self ) :
		name = self.name
		args = []
		if hasattr( self, "args" ) :
			args += map( lambda x: str( x ), self.args )
		if hasattr( self, "kvargs" ) :
			args += map( lambda item : str( item[ 0 ] ) + "=" + str( item[ 1 ] ), self.kvargs.items() )
		
		if args :
			name += "(" + ", ".join( args ) + ")"
		return name

	def Run( self, fx ) :
		args = ( fx, ) 
		if hasattr( self, "args" ) :
			args = args + self.args
		kvargs = {}
		if hasattr( self, "kvargs" ) :
			kvargs = self.kvargs

		self.func( *args, **kvargs )



class Fixture :

	def __init__( self, cls ) :
		self.testclass = cls
		self.name = cls.__name__
		self.tests = []
		for name, method in cls.__dict__.items() :
			if type( method ) == types.FunctionType :
				i = 0
				while i < len( g_funcs ) :
					fi = g_funcs[ i ]
					if fi.func == method :
						if fi.type == FuncType.Test :
							self.tests.append( TestEntity( name, method ) )
						elif fi.type == FuncType.TestCase :
							te = TestEntity( name, method )
							te.args = fi.args
							te.kvargs = fi.kvargs
							self.tests.append( te )
						elif fi.type == FuncType.Setup :
							self.setup = method
						elif fi.type == FuncType.Teardown :
							self.teardown = method
						elif fi.type == FuncType.FixtureSetup :
							self.fxsetup = method
						elif fi.type == FuncType.FixtureTeardown :
							self.fxteardown = method

						g_funcs.pop( i )
					else :
						i += 1
						

	def RunTests( self ) :
		fx = self.testclass()
		try :
			if hasattr( self, "fxsetup" ) :
				self.fxsetup( fx )

			for test in self.tests :
				

				print "==================="
				print self.name + " -- " + test.GetName()
				try :
					if hasattr( self, "setup" ) :
						self.setup( fx )
					try :
						test.Run( fx )
						print "OK"
					except Exception as e :
						print e
						print 
						print traceback.format_exc()

				except Exception as e :
					print "Setup failed"
					print e 
					print
					print traceback.format_exc()
				
				try :
					if hasattr( self, "teardown" ) :
						self.teardown( fx )
				except Exception as e :
					print "Teardown failed"
					print e 
					print
					print traceback.format_exc()
		
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
		print "==================="
		print test.func.func_name
		try :
			if test.type == FuncType.Test :
				test.func()
			else :
				test.func( *test.args, **test.kvargs )
			print "OK"
		except Exception as e :
			print e
			print 
			print traceback.format_exc()