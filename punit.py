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


class Fixture :

	def __init__( self, cls ) :
		self.testclass = cls
		self.name = cls.__name__
		self.tests = []
		for name, method in cls.__dict__.items() :
			if type( method ) == types.FunctionType :
				for i in g_funcs :
					if i.func == method :
						g_funcs.remove( i )
						if i.type == FuncType.Test :
							self.tests.append( TestEntity( name, method ) )
						elif i.type == FuncType.Setup :
							self.setup = method
						elif i.type == FuncType.Teardown :
							self.teardown = method
						elif i.type == FuncType.FixtureSetup :
							self.fxsetup = method
						elif i.type == FuncType.FixtureTeardown :
							self.fxteardown = method
						
						break

	def RunTests( self ) :
		fx = self.testclass()
		try :
			if hasattr( self, "fxsetup" ) :
				self.fxsetup( fx )

			for test in self.tests :
				print "==================="
				print self.name + " -- " + test.name
				try :
					if hasattr( self, "setup" ) :
						self.setup( fx )
				
					try :					
						test.func( fx )
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