#!/usr/bin/python

import sys
import os
import os.path
import json
from collections import OrderedDict

## Init values.
usageString =    'Usage: ' + os.path.basename(__file__) + ' [input file] [starting value] [offset value] [output file]'
startingValue =  0
offsetValue =    0
inputFilename =  'input.json'
outputFilename = 'output.json'

## Get input filename.
if len(sys.argv) < 2:
	print(usageString)
	sys.exit()
inputFilename = sys.argv[1]
if not os.path.exists(inputFilename):
	print('Please specify an input file that exists.')
	sys.exit()

## Get starting value.
if len(sys.argv) < 3:
	print(usageString)
	sys.exit()
try:
	startingValue = int(sys.argv[2])
except ValueError:
	print('Please specify an integer value for the starting value.')
	sys.exit()

## Get offset value.
if len(sys.argv) < 4:
	print(usageString)
	sys.exit()
try:
	offsetValue = int(sys.argv[3])
except ValueError:
	print('Please specify an integer value for the offset value.')
	sys.exit()

## Get output filename.
if len(sys.argv) >= 4:
	outputFilename = sys.argv[4]

## Done with arg validation, process the json.
print('Offsetting all fg/bg values higher than ' + str(startingValue) + ' by ' + str(offsetValue) + ' in file ' + inputFilename + '.')
inputFile = open(inputFilename, 'r')
loadedJson = json.loads(inputFile.read(), object_pairs_hook = OrderedDict)
inputFile.close()

offsetFg = 0
offsetBg = 0
for i in range(len(loadedJson['tiles-new'][0]['tiles'])):
	checkingJson = loadedJson['tiles-new'][0]['tiles'][i]
	if 'fg' in checkingJson and int(checkingJson['fg']) > startingValue:
		loadedJson['tiles-new'][0]['tiles'][i]['fg'] += offsetValue
		offsetFg += 1
	if 'bg' in checkingJson and int(checkingJson['bg']) > startingValue:
		loadedJson['tiles-new'][0]['tiles'][i]['bg'] += offsetValue
		offsetBg += 1

## Save the output.
outputFile = open(outputFilename, 'w')
outputFile.write(json.dumps(loadedJson, indent=2, separators=(',', ': ')))
outputFile.close()

## All done.
print('Offset ' + str(offsetFg) + ' fg and ' + str(offsetBg) + ' bg. File saved to ' + outputFilename + '.')