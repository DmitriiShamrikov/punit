from decorators import *
from assertions import *


@TestFixture
class TestClass :

	@TestCase( 1, 2 )
	def Lol( self, x, y ) :
		IsTrue( x + y > 0 )

	@Test
	def Lol1( self ):
		pass


if __name__ == "__main__" :
	RunTests()

