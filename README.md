# [pyex](pyex.py) -- Allows for methods that can be used with class str, etc.

## TLDR

`pyex` is a preprocessor. You write a `.pyex` file in just slightly
extended Python, then `pyex.py` processes that into Python in the actual
form Python wants, all without monkeypatching or otherwise compromising
execution reliability.

This is a Python v2 project. A v3 Python version, if you want it, is up
to you at this point.

## Somewhat More Verbosely

This project grew indirectly from my annoyance with Python that it does
not provide the ability to extend the built-in classes, particularly the
string class. I have often wanted to just do something to a string as a
method, mainly -- and I know this is a simple thing, but -- mainly
because I consistently tend to think this way...

    x = 'foo'.upper()

...rather than this way: 

    x = upper('foo')

I've had some discussions with some really well-informed Python types,
and they all assure me that you simply can't extend the built-in classes
without incurring a risk of actually breaking the Python interpreter.
Well. _That_ was bad news.

But eventually \(I'm old and slowing down a lot\) it dawned on me that
even if it was impossible in Python, who says it has to _be_ Python?
There's a ton of functionality in the C language that comes from a
preprocessor; why not a preprocessor for Python?

And so... `pyex`.

`pyex` means `Python, Extended` and that's exactly what it is. You write
using `pyex` syntax -- which is exactly the same as Python syntax --
except for two "little" things.

The first is that you can write a method and attach it to any class
object it is written to understand.

The second is that you declare this with a tiny bit of new syntax.

Here's a for-instance. Say you have a method that takes a string object
and validates that it is a dotted quad and you want to be able to use it
as a method on strings. Here's something you might write:

```Python
extend:testDottedQuad
def testDottedQuad(strObject):
	if type(strObject) != str: return False
	listStrings = strObject.split('.')
	if len(listStrings) != 4: return False
	for strNum in listStrings:
		try:	val = int(strNum)
		except:	return False
		if val < 0: return False
		if val > 255: return False
	return True
```

Now, at some point, you have a string in your program you'd like to
validate. Here are some of the things you can do via `pyex` with the
above in place:

```Python
if '192.168.1.100'.testDottedQuad():
	doSomething()

dq = '216.126.621.5'
if not dq.testDottedQuad():
	throwWarning();

dqt = ''.join(['127','.','0','.','0','.','1']).testDottedQuad()
if dqt:
	print 'well, that was fun'
```

Syntactically speaking, you can use these as extended methods on
strings, functions that return strings, and variables that contain
strings as if the methods were actual members of the string class. They
aren't, of course, so it's advisable to do some checking inside your
methods to make sure that they're receiving the kind of object they
expect.

The process is simple. First, you write a `.pyex` file that contains your
Python, plus this extended syntax. Then you run it through `pyex.py`.
`pyex.py`, in turn, will produce an output file in pure Python that has
changed the syntax to be normal function call based; this is the final
end product, what you actually run.

`pyex` strips comments, although if you ask it to, it will put your
original lines in as comments above the generated lines so you can
examine the metamorphosis from `pyex` to Python.

Basically that's it. Typing `pyex.py` by itself will generate help text.

## Syntax coloring / highlighting

I often edit Python \(and now, `pyex`\) in Midnight Commander's
`cooledit` editor. I've created a \(very\) slightly modifed syntax
highlighting file for `.pyex` files \(`pyex.syntax`\) for this editor by
taking the Python syntax file and adding the `extend` keyword. If you
are going to use `pyex`, I think you'll find it useful to implement a
syntax file for yoar editor as well, and most likely, you can do what I
did -- grab the Python syntax, modify it by adding one keyword, assign
the result to `pyex`, and done.

## Example Use

| Console input | Result |
| -------- | ------------ |
| pyex.py myStuff | myStuff.pyex --> myStuff.py |
| pyex.py myStuff.pyex | myStuff.pyex --> myStuff.py |
| pyex.py myStuff -o yourStuff | mystuff.pyex --> yourStuff.py |
| pyex.py myStuff.pyex -o herStuff | myStuff.pyex --> herStuff.py |
| pyex.py myStuff.pyex -o hisStuff.py | myStuff.pyex --> hisStuff.py |
| pyex.py myStuff -c | myStuff.pyex --> myStuff.py + your code inserted as comments in myStuff.py |
| pyex.py myStuff -c -b | myStuff.pyex --> myStuff.py + your code inserted as comments with leading blank lines in myStuff.py |
| pyex.py myStuff -v -b | myStuff.pyex --> myStuff.py + verbose dump of progress incorporating blank lines between conversions |
| pyex.py | You get a bunch of help about the options |

## Testing
Executing `test_pyex.py` will generate `pyextest.py` from `pyextest.pyex`
and compare the result with `expected.py`. If the results match, then
pyex.py is working at least as well for you as it does for me. If they
do _not_ match, a list of the differences will be provided and a warning
generated.

## Files

* pyex.py -- the preprocessor
* pyextest.pyex -- a test file you can run through pyex.py
* pyex.syntax -- a syntax file for Midnite Commander
* README.md -- this file
* test_pyex.py -- unit test
* expected.py -- base result for successful unit test

## Project Details
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
                 of pyex.py that incorporates accepted commits from others, you are risking
                 the use of OPC, which may or may not be protected by copyright, patent, and the
                 like, because our intellectual property system is pathological. The risks and
                 responsibilities and any subsequent consequences are entirely yours. Have you
                 written your congresscritter about patent and copyright reform yet?
  Incep Date: October 29th, 2016     (for Project)
 Last Update: October 30th, 2016     (for Project)
     Dev Env: OS X 10.6.8, Python 2.6.1
	  Status: BETA
```

