from decorators import *
from assertions import *


@TestFixture
class TestClass :

	@TestFixtureSetup
	def init( this ) :
		print "hi"

	@TestFixtureTeardown
	def shutdown( this ) :
		print "bye!"

	@TestMethod
	def TestFunction1( this ):
		#print "call TestClass.TestFunction1"
		IsTrue( False )

	@TestMethod
	def TestFunction2( this ) :
		#print "call TestClass.TestFunction2"
		AreEquals( 1, 1 )


if __name__ == "__main__" :
	RunTests()

