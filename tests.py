from decorators import *
from assertions import *


@TestFixture
class TestClass :

	@TestCase( 1, 2, k = 3, p = 4, skip=True )
	@TestCase( 3, 4 )
	def Lol( self, x, y, k = None, p = None ) :
		IsTrue( x + y > 0 )

	@Test
	def Lol1( self ):
		pass

@TestCase( 1, 2 )
def Lol( x, y ) :
	print x + y

if __name__ == "__main__" :
	RunAllTests()

