#!/usr/bin/python

import sys,os,re

# Globals
# -------
strSourceExt		= '.pyex'
strPermissions		= '755'
listMethods			= []
boolReportMethods	= False
boolReportPasses	= False
boolCommentSource	= False
boolReportSetup		= False
boolDoNotProcess	= False
boolVerbose			= False
boolBlankLines		= False

# These are token identities. They are used to
# class tokens for parsing and human-readability
# ----------------------------------------------
class sTokens:
	NUMBER		=  1
	STRING		=  2
	WHITESPACE	=  3
	NAME		=  4
	COMMA		=  5
	OPENPAREN	=  6
	CLOSEPAREN	=  7
	EQUALS		=  8
	OPENBRACE	=  9
	CLOSEBRACE	= 10
	OPENSQUARE	= 11
	CLOSESQUARE	= 12
	COLON		= 13
	SEMICOLON	= 14
	SPLAT		= 15
	LESSTHAN	= 16
	GREATERTHAN	= 17
	ASTERISK	= 18
	PLUSSIGN	= 19
	MINUSSIGN	= 20
	DIVIDESIGN	= 21
	PERCENTSIGN	= 22
	AMPERSAND	= 23

st = sTokens()

# Single token details
# ====================
# ...and by "single token" I mean in the context of pyex, which isn't
# concerned with compound tokens of the >= or && nature, only with dealing
# with getting them out of a source code line, and then putting them back
# the way they were found. pyex considers strings, alphanumeric
# identifiers, whitespace and numbers as the multi-character tokens it
# needs to be aware of.
#
# Technically, I could have gone with a bunch of individual whitespace
# tokens too, as they are not significant either. But I wrote it to treat
# them as units, and that works fine too.
#
# The period is a (very) special case, as it has roles in numbers, method
# attachments, and (rarely) in the ellipsis used with multi-dimensional
# slicing. So '.' is treated in the tokenizer in a more comprehensive way
# than these tokens, which I mainly need to recognize as valid Python.
# --------------------------------------------------------------------------
listSingTok = [
	[',',st.COMMA,'comma'],['(',st.OPENPAREN,'openParen'],
	[')',st.CLOSEPAREN,'closeParen'],['=',st.EQUALS,'equals'],
	['{',st.OPENBRACE,'openBrace'],['}',st.CLOSEBRACE,'closeBrace'],
	['[',st.OPENSQUARE,'openSquare'],[']',st.CLOSESQUARE,'closeSquare'],
	[':',st.COLON,'colon'],[';',st.SEMICOLON,'semiColon'],
	['!',st.SPLAT,'splat'],['<',st.LESSTHAN,'lessThan'],
	['>',st.GREATERTHAN,'greaterThan'],['*',st.ASTERISK,'asterisk'],
	['+',st.PLUSSIGN,'plusSign'],['-',st.MINUSSIGN,'minusSign'],
	['/',st.DIVIDESIGN,'divideSign'],['%',st.PERCENTSIGN,'percentSign'],
	['&',st.AMPERSAND,'ampersand']
]

# Produces human-readable string from token code
# ----------------------------------------------
def tokenClasser(intToken):
	global st
	for listTok in listSingTok:
		if intToken == listTok[1]:
			return listTok[2]
	return 'unknownTokenType'

# Identifies whitespace characters
# --------------------------------
def isWhiteSpace(strChar):
	if strChar in '\t\n\r\f ': return True
	return False

# Identifies numbers, which (almost) always start with
# a digit. Except for floats; and because the '.' has
# several other meanings in Python, it is dealt with
# algorithmically.
# ----------------------------------------------------
def isNumericStart(strChar):
	if strChar in '0123456789': return True
	return False

# Identifies numbers in positions past the first
# digit or '.'
# ----------------------------------------------
def isNumeric(strChar): # ints, hex/oct/bin, floats
	if strChar.upper() in '0123456789OXABCDEFL+-': return True
	return False

# Identifies characters that can start a name legally
# ---------------------------------------------------
def isLegalNameStart(strChar):
	if strChar.lower() in 'abcdefghijklmnopqrstuvwxyz_': return True
	return False

# Identifies characters that can be in a name past
# the starting character
# ------------------------------------------------
def isLegalNamePastStart(strChar):
	if isLegalNameStart(strChar) == 1: return True
	if isNumeric(strChar) == 1: return True
	if strChar == '_': return True
	return False

# Helper for parsing fail diagnosis
# ---------------------------------
def pfail(intIndex,intLineNumber,strLine):
	print 'Parsing Failed at line '+str(intLineNumber)
	strOut = ' ' * intIndex
	strOut += '|'
	print strOut
	strLine = strLine.replace('\t',' ')
	print strLine

# Generates a list of human-readable token names
# from a class list
# -----------------
def tokenReader(listClasses):
	out = ''
	for tok in listClasses:
		out += tokenClasser(tok)+','
	if out[-1] == ',':
		out = out[:-1]
	return out

# This takes a line of Python code and converts it into
# two lists: The first is a list containing what pyex
# sees as atomic tokens. Strings, names, numbers,
# whitespace, special characters. The second is a list
# of equal length that contains the identities of each
# of the tokens that can be used to parse the line,
# re-arranging the tokes, without reference to what
# is actually in each token.
# ----------------------------------------------------
def tokenizer(strLine,intLineNumber):
	global st
	global listSingTok
	listTokens = []
	listTokenClasses = []
	strToken = ''
	strInString = ''
	strLastChar = ''
	boolInWhiteSpace = False
	boolInName = False
	boolInNumber = False
	boolInString = False
	boolInToken = False
	intIndex = -1
	intLastMode = -1
	intFlagMode = -1
	intLineLen = len(strLine)

	for strChar in strLine:
		intIndex += 1
		while strChar != '':

			# First, if we're not currently accumulating a
			# multi-character entity, we check to see what
			# we did last. If it was tokenize a name, a string,
			# or close a set of parens (which might indicate
			# a function), then we're interested to see if
			# a period might be introducing a named extension
			# It also might be a number such as .123 which
			# we will not treat as a potentially extendable
			# entity.
			# -----------------------------------------------
			if	boolInWhiteSpace == False and \
				boolInName == False and \
				boolInNumber == False and \
				boolInString == False:
				boolOpenToken = False
				if strChar == '.': # could be a method; in which case, we open the token with a .
					if intFlagMode   == st.NAME:
						boolOpenToken = True
					elif intFlagMode == st.STRING:
						boolOpenToken = True
					elif intFlagMode == st.CLOSEPAREN:
						boolOpenToken = True
					else: # might be the beginning of a number...
						boolHalt = False
						# if room to look +/- 1 character here:
						if intIndex < intLineLen-1 and intIndex > 0:
							if not isNumericsStart(strLine[intIndex+1]): # and not number
								boolHalt = True
							# or an elipsis: '...' - rare, but part of Python
							elif not (strLine[intIndex+1] == '.' or \
										strLine[intIndex-1] == '.'):
								boolHalt = True
						else: # period at start or end of line
							boolHalt = True
						if boolHalt:
							print 'stray "." character in line '+str(intLineNumber)
							pfail(intIndex,intLineNumber,strLine)
							tokenReader(listTokenClasses)
							print str(listTokens)
							raise SystemExit
					if boolOpenToken:
						strToken = strChar
						strChar = ''
						intFlagMode = -1
				
				# Now we look to see if we need to start to
				# accumulate multi-character tokens: strings,
				# whitespace, names, numbers:
				# -------------------------------------------
				elif strChar == '"' or strChar == "'": # starting string
					intInToken = True
					boolInString = True
					strInString = strChar
					strToken = strChar
					strChar = ''
				elif isWhiteSpace(strChar):				# starting whitespace
					boolInToken = True
					boolInWhiteSpace = True
					strToken = strChar
					strChar = ''
				elif isLegalNameStart(strChar):			# starting name
					boolInToken = True
					boolInName = True
					strToken += strChar
					intFlagMode = st.NAME
					intLastMode = st.NAME
					strChar = ''
				elif isNumericStart(strChar):			# starting number
					boolInToken = True
					boolInNumber = True
					intLastMode = st.NUMBER
					strToken += strChar
					strChar = ''

				# Not a multi-character token, so check
				# for single character tokens:
				# -------------------------------------
				else:
					boolTokHit = False
					for listTok in listSingTok:
						strTok = listTok[0]
						intTok = listTok[1]
						if strChar == strTok:
							listTokenClasses += [intTok]
							listTokens += [strChar]
							intLastMode = intTok
							strChar = ''
							boolTokHit = True
							break

					# If whatever this is hasn't been ID'd yet,
					# it's probably something I missed tokenizing,
					# and so I need to know about it. Fail here
					# with enough info to find it:
					# -------------------------------------------
					if not boolTokHit:
						pfail(intIndex,intLineNumber,strLine)
						raise SystemExit

			# This else happens when the tokenizer is
			# accumulating one of a string, whitespace,
			# a name, or a number:
			# -----------------------------------------
			else: # we're accumulating something
				if boolInString:	# accumulating a string?
					if strLastChar != '\\': # only test non-escaped chars

						# strings terminate depending on how they
						# were opened: single and double quotes
						# must match so they can be embedded in
						# each other:
						# -----------------------------------------------
						if	(strInString == '"' and strChar == '"') or \
							(strInString == "'" and strChar == "'"):
							strToken += strChar
							strChar = ''
							listTokens += [strToken]
							strToken = ''
							boolInToken = False
							boolInString = False
							intLastMode = st.STRING
							intFlagMode = st.STRING
							listTokenClasses += [st.STRING]
						else:
							strToken += strChar
							strChar = ''
					else: # we accept backslash anything
						strToken += strChar
						strChar = ''

				elif boolInWhiteSpace:			# accumulating whitespace?
					if isWhiteSpace(strChar):
						strToken += strChar
						strChar = ''
					else:
						listTokens += [strToken]
						strToken = ''
						boolInToken = False
						boolInWhiteSpace = False
						intLastMode = st.WHITESPACE
						listTokenClasses += [st.WHITESPACE]

				elif boolInName:				# accumulating a name?
					if isLegalNamePastStart(strChar):
						strToken += strChar
						strChar = ''
					else:
						listTokens += [strToken]
						strToken = ''
						boolInName = False
						boolInToken = False
						intLastMode = st.NAME
						listTokenClasses += [st.NAME]

				elif boolInNumber:				# accumulating a number?
					if isNumeric(strChar):
						strToken += strChar
						strChar = ''
					else:
						listTokens += [strToken]
						strToken = ''
						boolInToken = False
						boolInNumber = False
						intLastMode = st.NUMBER
						listTokenClasses += [st.NUMBER]
				else: # shouldn't get here, but...
					print 'unknown parsing state!'
					raise SystemExit
		strLastChar = strChar
	return listTokenClasses,listTokens

# I get tired of writing sys.stdout.write(yadda)
# ----------------------------------------------
def w(strParam):
	sys.stdout.write(strParam)

# I get tired of writing "print", too. :)
# ---------------------------------------
def p(strParam):
	print strParam

# Prints a formatted line number, followed by the line
# ----------------------------------------------------
def pln(intLineNumber,strLine):
	strOut = '%6d' % (intLineNumber)
	w(strOut+': ')
	p(strLine)

# This covers various failures WRT to
# invocation of pyex.
# -----------------------------------
def error(intErrorNum,strData='',intLineNumber=-1):
	global strSourceExt
	if intErrorNum == 1:
		print 'pyex.py requires a source file as input'
	if intErrorNum == 2:
		print 'pyex.py requires a '+strSourceExt+' source file as input'
	if intErrorNum == 3:
		print '"'+strData+'" is not a complete file name'
	if intErrorNum == 4:
		print '"'+strData+'" could not be opened'
	if intErrorNum == 5:
		print '"'+strData+'" could not be closed'
	if intErrorNum == 6:
		print 'Bad method declaration "'+strData+'" in line number '+str(intLineNumber)
	if intErrorNum == 7:
		print '"'+strData+'" could not be opened for write'
	if intErrorNum == 8:
		print 'Could not chmod "'+strData+'"'
	if intErrorNum == 9:
		print 'Unknown Option: "'+strData+'"'
	if intErrorNum == 10:
		print '-o requires a filename'
	if intErrorNum == 11:
		print ''
	raise SystemExit

# This is the first of two passes. It receives a series
# of lines from the input file, and locates the 'extend: yadda'
# statements, building a list of methods so identified. These
# will be used in the second pass to identify uses of methods
# that are extended, while ignoring methods that are not.
# -------------------------------------------------------------
def pass1(intLineNumber,strLine,fhFilehandle=None):
	global listMethods
	if strLine[0] != '#' and len(re.findall('extend:',strLine)) == 1:
		strMethodName = strLine[7:].strip()
		if len(strMethodName) < 1:
			error(6,strLine,intLineNumber)
		listMethods += [strMethodName]

# This is the parser that takes the tokenized line and
# replaces pyex's fabulous extended syntax with Python's
# "having a Monday" mundane function calls.
# ----------------------------------------------------
def reTokenize(listTokens,listClasses,listMethods):
	global st
	intLength = len(listTokens)
	if intLength < 2: return listTokens
	for i in range(1,intLength):
		for strMethod in listMethods:
			tok = listTokens[i]
			if listClasses[i] == st.NAME:
				#           i
				#      3    4      56   78   9
				#  in: 'foo'.method(parm,parm)
				#  in: 'foo'.method()
				if listClasses[i-1] == st.STRING:	# this block only deals with basic strings
					if intLength - i > 1: # ensure there is room to lookahead
						if tok == '.'+strMethod:	# out: method('foo',parm,parm)
							tmp = listTokens[i-1]				# capture string
							listTokens[i-1] = listTokens[i][1:]	# throw method where string was
							listTokens[i] = listTokens[i+1]		# put paren after method
							if listTokens[i+2] != ')': # if params not empty
								tmp = tmp+','
							listTokens[i+1] = tmp				# put param as first term in method
				#       i
				#      34      56   78   9
				#  in: x.method(parm,parm)
				#  in: x.method()
				elif listClasses[i-1] == st.NAME:	# this block deals with variable names
					if intLength - i > 1: # ensure there is room to lookahead
						if tok == '.'+strMethod:	# out: method('foo',parm,parm)
							tmp = listTokens[i-1]				# capture name
							listTokens[i-1] = listTokens[i][1:]	# throw method where name was
							listTokens[i] = listTokens[i+1]		# put paren after method
							if listTokens[i+2] != ')': # if params not empty
								tmp = tmp+','
							listTokens[i+1] = tmp				# put param as first term in method
				#               i
				#      1       234      56   78   9
				#  in: function().method(parm,parm)
				#  in: function().method()
				#                                               i
				#   0     1    2    3    4    5       6    7    8         9    10
				# ['\t', 'x', ' ', '=', ' ', 'meth', '(', ')', '.test2', '(', ')']
				elif listClasses[i-1] == st.CLOSEPAREN:	# this block deals with function().method()
					if intLength - i > 1:				# ensure there is room to lookahead
						if tok == '.'+strMethod:
							intPCount = 1
							j = i-2
							while j > 0 and intPCount != 0:
								if listClasses[j] == st.CLOSEPAREN: intPCount += 1
								elif listClasses[j] == st.OPENPAREN: intPCount -= 1
								if intPCount != 0:
									j -= 1 # walk back
							if intPCount == 0: # parens are now balanced
								j -= 1
								k = i
								tmp = listTokens[i][1:] # save method name, minus the dot
								if listTokens[i+2] != ')': # if params not empty
									listTokens[k - 1] += ','
								# now move forward, writing precedents starting at open paren of method
								while k >= j:
									listTokens[k+1] = listTokens[k-1] # B --> A
									k -= 1
								listTokens[j] = tmp
								listTokens[j+1] = '('
								listTokens[j] = tmp # emplace method at from this mess
	return listTokens

# Takes an input line, tokenizes it, changes the
# object-attached methods into function calls, and
# the re-assembles the line in Python-compatible
# format
# ------------------------------------------------
def parseOutMethod(strLineLocal,listMethods,intLineNumber):
	listClasses,listTokens = tokenizer(strLineLocal,intLineNumber)
	listTokens = reTokenize(listTokens,listClasses,listMethods)
	foo = ''.join(listTokens)
	return foo

# This is pass two. It works through all the lines in the .pyex
# file and processes them using parseOutMethod(), above. It
# then actually writes them (and comments if that's wsitched on)
# to the output, and optionally the console as well.
# -------------------------------------------------------------
def pass2(intLineNumber,strLine,fhWriteFile):
	global boolCommentSource
	if len(re.findall('extend:',strLine)) == 1:
		pass
	else:
		if strLine[0] != '#':
			try:
				hit = 0
				for strMethod in listMethods:
					if strLine.find('.'+strMethod+'(') != -1:
						hit = 1
				if hit == 0:
					fhWriteFile.write(strLine+'\n')
				else:
					strBlank = ''
					if boolBlankLines:
						strBlank = '\n'
					strNewLine = parseOutMethod(strLine,listMethods,intLineNumber)
					if boolCommentSource:
						fhWriteFile.write(strBlank+'# '+strLine+'\n')
					fhWriteFile.write(strNewLine+'\n')
					if boolVerbose:
						print strBlank+'# '+strLine
						print strNewLine
					
			except Exception,e:
				print str(intLineNumber) +': '+ str(e)
				raise
		else: # comment line
			if len(strLine) > 2:
				if strLine[1] == '!':
					if strLine.find('pyex.py') == -1:
						fhWriteFile.write(strLine+'\n')

# This runs a pass, stripping comments and passing along each line
# ----------------------------------------------------------------
def dopass(fhFile,funcPass,fhWriteFile=None):
	fhFile.seek(0)
	intLineNumber = 1
	for strLine in fhFile:
		strLine = strLine.rstrip()
		listLine = strLine.split('#')
		if len(strLine) > 0 and strLine[0] == '#' or listLine[0] != '':
			if strLine[0] != '#':
				strLine = listLine[0]
				strLine = strLine.rstrip()
			funcPass(intLineNumber,strLine,fhWriteFile)
		intLineNumber += 1

# console-level command syntax help()
# -----------------------------------
def help(strName):
	print strName+' Usage:'
	print strName+' source.pyex[ -o newname[.py]][ -p][ -e][ -c]'
	print '[-o newname[.py]] changes source.pyex --> source.py'
	print '                       to source.pyex --> newname.py'
	print '[ -p] pass information will be printed'
	print '[ -e] extended method names will be printed'
	print '[ -c] unmodified source lines as comments in output'
	print '[ -r] report setup before processing'
	print '[ -x] do not process (intended for use with [ -r])'
	print '[ -v] verbose output of each extended translation'
	raise SystemExit

# ===================================================================== #
# --------------------------------------------------------------------- #
# Code Execution Begins here (other than setting up the globals up top) #
# --------------------------------------------------------------------- #
# ===================================================================== #

# Parse out command line arguments
# --------------------------------
strWriteFileName = ''
strSourceFile = ''
if len(sys.argv) < 2:
	help(sys.argv[0])
argc = len(sys.argv)
boolNewo = False
boolHito = False
boolHits = False
strSourceFile = ''
for i in range(1,argc):
	strParm = sys.argv[i]
	if boolHito == True:
		if strParm[-3:] != '.py':
			strParm += '.py'
		strWriteFileName = strParm
		boolHito = False
		boolNewo = True
	else:
		if strParm == '-o':
			boolHito = True
		elif strParm == '-r':
			boolReportSetup = True
		elif strParm == '-x':
			boolDoNotProcess = True
		elif strParm == '-e':
			boolReportMethods = True
		elif strParm == '-v':
			boolVerbose = True
		elif strParm == '-b':
			boolBlankLines = True
		elif strParm == '-c':
			boolCommentSource = True
		elif strParm == '-p':
			boolReportPasses = True
		else:
			if i == 1:
				strSourceFile = strParm
				boolHits = True
			else:
				error(9,strParm)

if strSourceFile[-5:] != strSourceExt:
	strSourceFile += strSourceExt

if boolNewo == False:
	strWriteFileName = strSourceFile[:-5]+'.py'

if strSourceFile[:-5] == '':
	error(3,strSourceFile)

if boolReportSetup:
	print '       args:'+str(sys.argv)
	print '     source:'+strSourceFile
	print '       dest:'+strWriteFileName
	print '     method:'+str(boolReportMethods)
	print '     passes:'+str(boolReportPasses)
	print '   comments:'+str(boolCommentSource)
	print '     report:'+str(boolReportSetup)
	print '       stop:'+str(boolDoNotProcess)
	print '    verbose:'+str(boolVerbose)
	print ' blanklines:'+str(boolBlankLines)

if boolDoNotProcess:
	raise SystemExit

if boolHito == True:
	error(10)

# File Processing begins
# ----------------------
try:
	fhSourceFile = open(strSourceFile)
except:
	error(4,strSourceFile)

# Pass 1: Locate all methods
# --------------------------
if boolReportPasses: p('Pass 1...')
dopass(fhSourceFile,pass1)
if boolReportPasses: p('Pass 2...')
try:
	fhWriteFile = open(strWriteFileName,'w')
	dopass(fhSourceFile,pass2,fhWriteFile)
	fhWriteFile.close()
	strParm = 'chmod '+strPermissions+' '+strWriteFileName
	try:
		os.system(strParm)
	except:
		error(8,strParm)
except Exception,e:
	print str(e)
	error(7,strWriteFileName)

# File processing ends
# --------------------
try:
	fhSourceFile.close()
except:
	error(5,strSourceFile)

# This is kind of like a symbol table dump
# from an assembler or linker
# ----------------------------------------
if boolReportMethods:
	if boolReportPasses: print
	print 'Methods:'
	for strMethodName in listMethods:
		print '    '+strMethodName
