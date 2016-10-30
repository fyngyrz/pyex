# [pyex](pyex.py) -- Adds static methods that can be added to class str, etc.

This project grew, somewhat indirectly, from my annoyance with Python that it
does not provide the ability to extend the built-in classes, particularly
the string class. I have often wanted to just do something to a string as a
method, mainly -- and I know this is a simple thing, but -- mainly because
I think this way...

    x = 'foo'.upper()

...rather than this way: 

    x = upper('foo')

I've had some discussions with some really well-informed Python types,
and they all assure me that you simply can't extend the built-in classes
without taking the risk of actually breaking the Python interpreter.
Well. _That_ was bad news.

But eventually \(I'm old and slowing down a lot\) it dawned on me that
even if it was impossible in Python, who says it has to _be_ Python?
There's a ton of functionality in the C language that comes from a
preprocessor; why not a preprocessor for Python?

And so pyex was born.

pyex means `Python, Extended` and that's exactly what it is. You write
using pyex syntax -- which is exactly the same as Python syntax --
except for two "little" things.

The first is that you can write a method and attach it to any class
object it is written to understand.

The second is that you declare this with a tiny bir of new syntax.

Here's a for instance. Say you have a method that takes a string object
and validates that it is a dotted quad and you want to be able to use it
as a mthod on strings. Here's what you do:

	extend: testDottedQuad
    def testDottedQuad(strObject):
		if (...) return True
		return False

Now, at some point, you have a string in your program you'd like to
validate. Here are some of the things you can do in pyex:

	if '192.168.1.100'.testDottedQuad():
		doSomething()

    dq = '216.126.621.5'
	if !dq.testDottedQuad():
		throwWarning();

	dq = ''.join(['127','.','0','.','0','.','1']).testDottedQuad()

Basically, you can use these extended methods on strings, functions, and
variables as if it was an actual member of the string class.

The process is simple. First, you write a .pyex file that contains your
Python, plus this extended syntax. Then you run it through pyex.py.
pyex.py, in turn, will produce an output file in pure Python that has
changed the syntax to be normal function call based; this is the final
end product, what you actually run.

pyex strips comments, although if you ask it to, it will put your
original lines in as comments above the generated lines so you can
examine the metamorphosis from pyex to Python.

Basically that's it. pyex by itself will generate help text.

Here are some examples of use:

| You Type | This Happens |
| -------- | ------------ |
| pyex myStuff | myStuff.pyex --> myStuff.py |
| pyex myStuff.pyex | myStuff.pyex --> myStuff.py |
| pyex myStuff -o yourStuff | mystuff.pyex --> yourStuff.py |
| pyex myStuff.pyex -o herStuff | myStuff.pyex --> herStuff.py |
| pyex myStuff.pyex -o hisStuff.py | myStuff.pyex --> hisStuff.py |
| pyex myStuff -c | myStuff.pyex --> myStuff.py + your code inserted as comments in myStuff.py |
| pyex | You get a bunch of help about the options |
