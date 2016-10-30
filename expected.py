#!/usr/bin/python
def test1(strObject,strS1,strS2):
	return strObject + strS1 + strS2
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
def shorty(strObject):
	if len(strObject) < 8: return True
	return False
def test2(strObject):
	return '"'+strObject+'"' + ' is ' + str(len(strObject)) + ' characters long'
def meth():
	return 'blue'
def zombie():
	return 'white'
def upup(strObject):
	return strObject.upper()
def test():
	print 'bah:'
# 	print 'foo:'.test1(" there's a method",' to my madness')
	print test1('foo:'," there's a method",' to my madness')
# 	print 'bing:'.test2()
	print test2('bing:')
test()
if 1:
	x = 'a'
# 	print x.test1('b','c')
	print test1(x,'b','c')
	fruit = 'cherries'
# 	print fruit.test1(' ripe',' and luscious')
	print test1(fruit,' ripe',' and luscious')
# 	print meth().test2();print zombie().test2()
	print test2(meth());print test2(zombie())
# 	print upup(meth()).test2()
	print test2(upup(meth()))
# 	print upup(meth()).test1(' red',' green')
	print test1(upup(meth()),' red',' green')
# 	print upup(str(['1','2','3'])).test2()
	print test2(upup(str(['1','2','3'])))
# 	print upup(str({1:'a',2:'b',3:'c'})).test2()
	print test2(upup(str({1:'a',2:'b',3:'c'})))
	z = {1:'ab',2:'bc',3:'cd'}
# 	print upup(str(z[2])).test2()
	print test2(upup(str(z[2])))
	y = {'a':1,'b':2,'c':3}
# 	print upup(str(z[y['c']])).test2()
	print test2(upup(str(z[y['c']])))
# 	print meth().test2()
	print test2(meth())
# 	print upup('foo').test2();print upup('bar').test2()
	print test2(upup('foo'));print test2(upup('bar'))
# 	print upup('foo').test2();print upup('bar').test1(' twice',' two')
	print test2(upup('foo'));print test1(upup('bar'),' twice',' two')
# 	if upup('boink').shorty():
	if shorty(upup('boink')):
		print 'Short!'
	else:
		print 'not Short'
# 	if not upup('boink').shorty():
	if not shorty(upup('boink')):
		print 'Long'
	else:
		print 'not Long'
# 	print str('127.0.0.1'.testDottedQuad())
	print str(testDottedQuad('127.0.0.1'))
# 	print str('password'.testDottedQuad())
	print str(testDottedQuad('password'))
# 	print str('4'.testDottedQuad())
	print str(testDottedQuad('4'))
# print "bar:".test1(' but',' no dir() and no help()')
print test1("bar:",' but',' no dir() and no help()')
