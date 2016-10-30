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

The second is that you declare this with a tiny bit of new syntax.

Here's a for instance. Say you have a method that takes a string object
and validates that it is a dotted quad and you want to be able to use it
as a method on strings. Here's what you write:

```Python
extend:testDottedQuad
def testDottedQuad(strObject):
	if type(strObject) != str: return False
	listStrings = strObject.split('.')
	if len(listStrings) != 4: return False
	for num in listStrings:
		try:
			val = int(num)
		except:
			return False
		if val < 0: return False
		if val > 255: return False
	return True
```

Now, at some point, you have a string in your program you'd like to
validate. Here are some of the things you can do in pyex:

```Python
if '192.168.1.100'.testDottedQuad():
	doSomething()

dq = '216.126.621.5'
if not dq.testDottedQuad():
	throwWarning();

dq = ''.join(['127','.','0','.','0','.','1']).testDottedQuad()
```

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

```
Application to provide extended Python syntax for methods on built-in classes
Most particularly, string.

      Author: fyngyrz  (Ben)
     Contact: fyngyrz@gmail.com (bugs, feature requests, kudos, bitter rejections)
     Project: pyex.py
    Homepage: https://github.com/fyngyrz/pyex
     License: None. It's free. *Really* free. Defy invalid social and legal norms.
 Disclaimers: 1) Probably completely broken. Do Not Use. You were explicitly warned. Phbbbbt.
              2) My code is blackbox, meaning I wrote it without reference to other people's code
              3) I can't check other people's contributions effectively, so if you use any version
                 of aa_macro.py that incorporates accepted commits from others, you are risking
                 the use of OPC, which may or may not be protected by copyright, patent, and the
                 like, because our intellectual property system is pathological. The risks and
                 responsibilities and any subsequent consequences are entirely yours. Have you
                 written your congresscritter about patent and copyright reform yet?
  Incep Date: October 29th, 2016     (for Project)
 Last Update: October 29th, 2016     (for Project)
     Dev Env: OS X 10.6.8, Python 2.6.1
	  Status:  BETA
```

## Files

* pyex.py -- the preprocessor
* pyextest.pyex -- a test file you can run through pyex.py
* pyex.syntax -- a syntax file for Midnite Commander
* README.md -- this file
