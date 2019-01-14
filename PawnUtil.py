#!/usr/bin/python

import sys
import os
import os.path
import json
from collections import OrderedDict

## Init values.
usageString =    'Usage: ' + os.path.basename(__file__) + ' [input file] [starting value] [offset value] [output file]'
offsets = { 'fg': 0, 'bg': 0 }

def updateFgAndBgValuesInList(input_list, offsetValue, startingValue):
	for ind in range(len(input_list)):
		for keyStr in offsets:
			if keyStr in input_list[ind]:
				try:
					if type(input_list[ind][keyStr]) is list:
						for subind in range(len(input_list[ind][keyStr])):
							if int(input_list[ind][keyStr][subind]) > startingValue:
								input_list[ind][keyStr][subind] += offsetValue
								offsets[keyStr] += 1
					else:
						if int(input_list[ind][keyStr]) > startingValue:
							input_list[ind][keyStr] += offsetValue
							offsets[keyStr] += 1
				except ValueError:
					print('Invalid value in JSON parse (ind ' + str(ind) + ', key ' + keyStr + ') - not int or list.')
		if 'additional_tiles' in input_list[ind]:
			updateFgAndBgValuesInList(input_list[ind]['additional_tiles'], offsetValue, startingValue)

def main():

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

	if 'tiles-new' in loadedJson and 'tiles' in loadedJson['tiles-new'][0]:
		updateFgAndBgValuesInList(loadedJson['tiles-new'][0]['tiles'], offsetValue, startingValue)
	else:
		print("Malformed JSON in input file, check your tile data.")
		sys.exit()

	## Save the output.
	outputFile = open(outputFilename, 'w')
	outputFile.write(json.dumps(loadedJson, indent=2, separators=(',', ': ')))
	outputFile.close()

	## All done.
	print('Offset ' + str(offsets['fg']) + ' fg and ' + str(offsets['bg']) + ' bg. File saved to ' + outputFilename + '.')

if __name__ == '__main__':
	main()