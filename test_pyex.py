#!/usr/bin/python

import unittest
import difflib
import sys
import os

def diffme(fra,frb):
	fa = fra.splitlines(1)
	fb = frb.splitlines(1)

	d = difflib.Differ()

	result = list(d.compare(fa, fb))

	for line in result:
		if line[0] != ' ':
			sys.stdout.write(line)

	print 'End of differences'

class TestPyEx(unittest.TestCase):

	def test_pyex(self):
		"""
Test pyex.py functionality
"""
		os.system('clear')
		expect	= 'expected.py'
		out		= 'pyextest'

		fh = open(expect)
		expected = fh.read()
		fh.close()

		os.system('./pyex.py '+out+' -c')
		fh = open(out+'.py')
		output = fh.read()
		fh.close()

		result = False
		if expected == output:
			result = True
		else:
			diffme(expected,output)

		try:
			self.assertEqual(True,result,'expected != output\nCompare expected.py with pyextest.py')
		except Exception,e:
			print 'Problem: '+str(e)
		else:
			print 'Test Passed'

if __name__ == '__main__':
	unittest.main()
