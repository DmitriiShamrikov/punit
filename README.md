This is a simple test framework, inspired by NUnit for C#. The goal of the framework is creating tests with nice notation using attributes/decorators like in NUnit.

Punit uses decorators to identify test functions, for example:
```python
@Test
def CheckSomething() :
    pass

@TestCase( 2, 2, 4 )
def CheckSum( arg1, arg2, expected ) :
    actual = arg1 + arg2
    AreEqual( expected, actual )
```