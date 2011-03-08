#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from consolecolors import *
import sys
from os import unlink, rename
from os.path import isfile, islink
from re import search

followSymLinks	= False
spacesCount		= 4
clearEmptyLines	= True
debugOutput		= False
keepOriginal	= False
copyUidGid		= False		# Not emplemented yet
copyPermissions	= False		# Not emplemented yet
spaces2tabs		= True		# False if tabs to spaces ;-)
tempFilePattern	= '%s.my.swp'
stripRight		= True		# Strip right side of each line


# Check input params from command line
if len(sys.argv) ==1:
	sys.exit('No files specified')

files = []
for fn in sys.argv[1:]:
	if not isfile(fn):
		print('%sWarning: %s%s%s is not regular file' % (C_RED, C_YELLOW, fn, C_CANCEL))
	elif islink(fn) and not followSymLinks:
		print('%sWarning: %s%s%s is symbolic link to another file' % (C_RED, C_YELLOW, fn, C_CANCEL))
	else:
		files.append(fn)
if not files:
	sys.exit('No files specified')

if not search('[^0-9]', sys.argv[-1]):
	spacesCount = int(sys.argv[-1])

# Processing files
print('%sProcessing %s%d file(s)%s' % (C_LBLUE, C_WHITE, len(files), C_CANCEL))

if spaces2tabs:
	strSearch, strReplace = (' ' * spacesCount, '\t')
else:
	strSearch, strReplace = ('\t', ' ' * spacesCount)

totalEmptyLines	= 0
totalMatchLines	= 0
totalCutLines	= 0
totalLines		= 0
totalSkipLines	= 0

for fn in files:
	try:
		f = open(fn, 'a+')
	except Exception as why:
		print('%sWarning: error was occured while opening file %s - %s' % (C_RED, fn, why,))

	if f:
		f.seek(0)
		proceeded = False
		newFn = tempFilePattern % fn
		try:
			newFile = open(newFn, 'w')
		except Exception as why:
			print('%sWarning: error was occured while opening %s fo write - %s' % (C_RED, newFn, why,))

		if newFile:
			print('%s%s%s in %sprogress%s ...' % (C_YELLOW, fn, C_WHITE, C_GREEN, C_CANCEL), end=' ')
			emptyLines	= 0
			cutLines	= 0
			line = f.readline()
			while line:
				newLine = line
				totalLines = totalLines + 1
				workLine = line.rstrip()
				if not workLine:
					emptyLines = emptyLines + 1
					newLine = '\n'
					if debugOutput:
						print('%sDEBUG: %s%d%s empty lines' % (C_VIOLET, C_YELLOW, emptyLines, C_CANCEL))
				elif workLine[0] in ['\t', ' ']:
					totalMatchLines = totalMatchLines + 1
					match = search('[^\t ]', line)
					newLine = line[:match.start()].replace(strSearch, strReplace) + line[match.start():]
					if newLine != line:
						cutLines = cutLines + 1
					if debugOutput:
						print('%sDEBUG: %s%d -> %d' % (C_VIOLET, C_CANCEL, len(line), len(newLine),))
				else:
					totalSkipLines = totalSkipLines + 1

				if workLine:
					newFile.write(newLine.rstrip() + '\n')
				else:
					newFile.write(newLine)
				line = f.readline()

			totalEmptyLines	= totalEmptyLines + emptyLines
			totalCutLines	= totalCutLines + cutLines

			newFile.close()
			proceeded = True
		f.close()
		if proceeded and not keepOriginal:
			unlink(fn)
			rename(newFn, fn)
		print('%sok%s' % (C_BLUE, C_CANCEL))

print('*' * 30 + '\n\033[32;1mSUMMARY:\033[0m\033[1m\ntotal       - %d\nskip lines  - %d\nempty lines - %d\nmatch lines - %d\ncut lines   - %d\n\033[0m' %\
	(totalLines, totalSkipLines, totalEmptyLines, totalMatchLines, totalCutLines,) + '*' * 30)

