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
NUMBER = 1
STRING = 2
WHITESPACE = 3
NAME = 4
COMMA = 5
OPENPAREN = 6
CLOSEPAREN = 7
EQUALS = 8
OPENBRACE = 9
CLOSEBRACE = 10
OPENSQUARE = 11
CLOSESQUARE = 12
COLON = 13
SEMICOLON = 14


def isWhiteSpace(strChar):
	if strChar in '\t\n\r ': return 1
	return 0

def isNumeric(strChar):
	if strChar in '0123456789': return 1
	return 0

def isLegalNameStart(strChar):
	if strChar.lower() in 'abcdefghijklmnopqrstuvwxyz_': return True
	return False

def isLegalNamePastStart(strChar):
	if isLegalNameStart(strChar) == 1: return True
	if isNumeric(strChar) == 1: return True
	if strChar == '_': return True
	return False

def isLegalName(strName):
	for strChar in strName:
		if strChar.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789_':
			return True
	return False

def pfail(intIndex,intLineNumber,strLine):
	print 'Parsing Failed at line '+str(intLineNumber)
	strOut = ' ' * intIndex
	strOut += '|'
	print strOut
	strLine = strLine.replace('\t',' ')
	print strLine

def tokenClasser(intToken):
	global NUMBER,STRING,WHITESPACE,NAME,COMMA,OPENPAREN,CLOSEPAREN,EQUALS,OPENBRACE,CLOSEBRACE,OPENSQUARE,CLOSESQUARE,COLON,SEMICOLON

	if intToken == NUMBER: return 'number'
	if intToken == STRING: return 'string'
	if intToken == WHITESPACE: return 'whiteSpace'
	if intToken == NAME: return 'name'
	if intToken == COMMA: return 'comma'
	if intToken == OPENPAREN: return 'openParen'
	if intToken == CLOSEPAREN: return 'closeParen'
	if intToken == EQUALS: return 'equals'
	if intToken == OPENBRACE: return 'openBrace'
	if intToken == CLOSEBRACE: return 'closeBrace'
	if intToken == OPENSQUARE: return 'openSquare'
	if intToken == CLOSESQUARE: return 'closeSquare'
	if intToken == SEMICOLON: return 'semiColon'
	if intToken == COLON: return 'colon'
	return 'unknownTokenType'

def tokenReader(listClasses):
	out = ''
	for tok in listClasses:
		out += tokenClasser(tok)+','
	if out[-1] == ',':
		out = out[:-1]
	return out

# World's dumbest Pythonesque tokenizer
# -------------------------------------
def tokenizer(strLine,intLineNumber):
	global NUMBER,STRING,WHITESPACE,NAME,COMMA,OPENPAREN,CLOSEPAREN,EQUALS,OPENBRACE,CLOSEBRACE,OPENSQUARE,CLOSESQUARE,COLON,SEMICOLON
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
	
	for strChar in strLine:
		intIndex += 1
		while strChar != '':
			if	boolInWhiteSpace == False and \
				boolInName == False and \
				boolInNumber == False and \
				boolInString == False:
				if strChar == '.': # could be a method; in which case, we open the token with a .
					if intFlagMode == NAME:
						strToken = strChar
						strChar = ''
						intFlagMode = -1
					elif intFlagMode == STRING:
						strToken = strChar
						strChar = ''
						intFlagMode = -1
					elif intFlagMode == CLOSEPAREN:
						strToken = strChar
						strChar = ''
						intFlagMode = -1
					else:
						print 'stray "." character in line '+str(intLineNumber)
						pfail(intIndex,intLineNumber,strLine)
						tokenReader(listTokenClasses)
						print str(listTokens)
						raise SystemExit
				
				elif strChar == '(':	# these have to tokenize immediately because they could be last
					listTokenClasses += [OPENPAREN]
					listTokens += [strChar]
					intLastMode = OPENPAREN
					strChar = ''
				elif strChar == ')':
					listTokenClasses += [CLOSEPAREN]
					listTokens += [strChar]
					intLastMode = CLOSEPAREN
					intFlagMode = CLOSEPAREN
					strChar = ''
				elif strChar == '{':
					listTokenClasses += [OPENBRACE]
					listTokens += [strChar]
					intLastMode = OPENBRACE
					strChar = ''
				elif strChar == '}':
					listTokenClasses += [CLOSEBRACE]
					listTokens += [strChar]
					intLastMode = CLOSEBRACE
					strChar = ''
				elif strChar == '[':
					listTokenClasses += [OPENSQUARE]
					listTokens += [strChar]
					intLastMode = OPENSQUARE
					strChar = ''
				elif strChar == ']':
					listTokenClasses += [CLOSESQUARE]
					listTokens += [strChar]
					intLastMode = CLOSESQUARE
					strChar = ''
				elif strChar == '=':
					listTokenClasses += [EQUALS]
					listTokens += [strChar]
					intLastMode = EQUALS
					strChar = ''
				elif strChar == ':':
					listTokenClasses += [COLON]
					listTokens += [strChar]
					intLastMode = COLON
					strChar = ''
				elif strChar == ';':
					listTokenClasses += [SEMICOLON]
					listTokens += [strChar]
					intLastMode = SEMICOLON
					strChar = ''
				elif strChar == ',':
					listTokenClasses += [COMMA]
					listTokens += [strChar]
					intLastMode = COMMA
					strChar = ''
				
				elif strChar == '"' or strChar == "'":
					intInToken = True
					boolInString = True
					strInString = strChar
					strToken = strChar
					strChar = ''
				elif isWhiteSpace(strChar):
					boolInToken = True
					boolInWhiteSpace = True
					strToken = strChar
					strChar = ''
				elif isLegalNameStart(strChar):
					boolInToken = True
					boolInName = True
					strToken += strChar
					intFlagMode = NAME
					intLastMode = NAME
					strChar = ''
				elif isNumeric(strChar):
					boolInToken = True
					boolInNumber = True
					intLastMode = NUMBER
					strToken += strChar
					strChar = ''
				else: # no idea... dump out with indicator
					pfail(intIndex,intLineNumber,strLine)
					raise SystemExit
			else: # we're accumulating something
				if boolInString:
					if strLastChar != '\\':
						if	(strInString == '"' and strChar == '"') or \
							(strInString == "'" and strChar == "'"):
							strToken += strChar
							strChar = ''
							listTokens += [strToken]
							strToken = ''
							boolInToken = False
							boolInString = False
							intLastMode = STRING
							intFlagMode = STRING
							listTokenClasses += [STRING]
						else:
							strToken += strChar
							strChar = ''
					else: # we accept backslash anything
						strToken += strChar
						strChar = ''
				elif boolInWhiteSpace:
					if isWhiteSpace(strChar):
						strToken += strChar
						strChar = ''
					else:
						listTokens += [strToken]
						strToken = ''
						boolInToken = False
						boolInWhiteSpace = False
						intLastMode = WHITESPACE
						listTokenClasses += [WHITESPACE]
				elif boolInName:
					if isLegalNamePastStart(strChar):
						strToken += strChar
						strChar = ''
					else:
						listTokens += [strToken]
						strToken = ''
						boolInName = False
						boolInToken = False
						intLastMode = NAME
						listTokenClasses += [NAME]
				elif boolInNumber:
					if isNumeric(strChar):
						strToken += strChar
						strChar = ''
					else:
						listTokens += [strToken]
						strToken = ''
						boolInToken = False
						boolInNumber = False
						intLastMode = NUMBER
						listTokenClasses += [NUMBER]
				else:
					print 'unknown parsing state!'
					raise SystemExit
		strLastChar = strChar
	return listTokenClasses,listTokens

def w(strParam):
	sys.stdout.write(strParam)

def p(strParam):
	print strParam

def pln(intLineNumber,strLine):
	strOut = '%6d' % (intLineNumber)
	w(strOut+': ')
	p(strLine)

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

# Parse out the method names
# --------------------------
def pass1(intLineNumber,strLine,fhFilehandle=None):
	global listMethods
	if strLine[0] != '#' and len(re.findall('extend:',strLine)) == 1:
		strMethodName = strLine[7:].strip()
		if len(strMethodName) < 1:
			error(6,strLine,intLineNumber)
		listMethods += [strMethodName]

def reTokenize(listTokens,listClasses,listMethods):
	global NUMBER,STRING,WHITESPACE,NAME,COMMA,OPENPAREN,CLOSEPAREN,EQUALS,OPENBRACE,CLOSEBRACE,OPENSQUARE,CLOSESQUARE,COLON,SEMICOLON
	intLength = len(listTokens)
	if intLength < 2: return listTokens
	for i in range(1,intLength):
		for strMethod in listMethods:
			tok = listTokens[i]
			if listClasses[i] == NAME:
				#           i
				#      3    4      56   78   9
				#  in: 'foo'.method(parm,parm)
				#  in: 'foo'.method()
				if listClasses[i-1] == STRING:	# this block only deals with basic strings
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
				elif listClasses[i-1] == NAME:	# this block deals with variable names
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
				elif listClasses[i-1] == CLOSEPAREN:	# this block deals with function().method()
					if intLength - i > 1:				# ensure there is room to lookahead
						if tok == '.'+strMethod:
							intPCount = 1
							j = i-2
							while j > 0 and intPCount != 0:
								if listClasses[j] == CLOSEPAREN: intPCount += 1
								elif listClasses[j] == OPENPAREN: intPCount -= 1
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

def parseOutMethod(strLineLocal,listMethods,intLineNumber):
	listClasses,listTokens = tokenizer(strLineLocal,intLineNumber)
	strTokenList = ''
	strPrePre = '['
	for tok in listClasses:
		strTokenList += strPrePre+tokenClasser(tok)
		strPrePre = ','
	strTokenList += ']'
	listTokens = reTokenize(listTokens,listClasses,listMethods)
	foo = ''.join(listTokens)
	return foo

# Method names are defined
# Replace method-style invocations with function-style invocations
# ----------------------------------------------------------------
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
					strNewLine = parseOutMethod(strLine,listMethods,intLineNumber)
					if boolCommentSource:
						fhWriteFile.write('# '+strLine+'\n')
					fhWriteFile.write(strNewLine+'\n')
					
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
	raise SystemExit

# Basic argument sanity checking
# ------------------------------
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
	print '    args:'+str(sys.argv)
	print '  source:'+strSourceFile
	print '    dest:'+strWriteFileName
	print '  method:'+str(boolReportMethods)
	print '  passes:'+str(boolReportPasses)
	print 'comments:'+str(boolCommentSource)
	print '  report:'+str(boolReportSetup)
	print '    stop:'+str(boolDoNotProcess)

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

if boolReportMethods:
	if boolReportPasses: print
	print 'Methods:'
	for strMethodName in listMethods:
		print '    '+strMethodName
