from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.pylab import * 
import numpy as np
import re


def analyzeSource(sourceFile, maxWordLength):
	'''Parse the source file for all words'''
	f = open(sourceFile, 'r')
	all_words = f.readlines()

	stringIndex = {}
	characterCounts = defaultdict(int)

	for j in range(maxWordLength-1):
		stringIndex[j] = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0,}

	for word in list(all_words):
		testChars = ''.join(word.split())
		for k in range(0, len(testChars)):
				stringIndex[k][testChars[k]] += 1

	return stringIndex
	
	
def normalize(sourceDicts):
	'''Normalize the given dictionaries'''
	newVals = []
	for i in range(len(sourceDicts)):
		sum = 0
		newVals.append([])
		for letter in  sorted(sourceDicts[i].items()):
			sum+= letter[1]
		print (sum)
		for letter in  sorted(sourceDicts[i].items()):
			newVals[i].append(letter[1] / sum)
	return newVals
	
def normalize2(sourceList):
	'''Actually normalize the initial normalize() results'''
	newVals = []
	for i in range(len(sourceList)):
		min = 1
		max = 0
		newVals.append([])
		for letterVal in  sourceList[i]:
			if letterVal > max:
				max=letterVal
			if letterVal < min:
				min = letterVal
		for letterVal in  sourceList[i]:
			newVals[i].append((letterVal - min)/(max - min))
	return newVals

		
def charRange(c1, c2):
	'''Generate a character range'''
	characters = []
	for c in range(ord(c1), ord(c2)+1):
		characters.append(str(chr(c)))
	return characters	
	
	
def cleanText(sourceFile, newFileName):
	file= open(sourceFile, 'r')
	text = file.read().lower()
	file.close()
	# replaces anything that is not a lowercase letter, a space, or an apostrophe with a space:
	text = re.sub('[^a-z\ \']+', " ", text)
	words = list(text.split())
	noApos = []
	for word in words:
		noApos.append(word.replace('\'', '') ) 
	unique_words = set(noApos)
	file = open('output.txt', 'w+')
	
	for word in unique_words:
		file.write(str(word) + "\n")
	return
	
	
#Main Flow
cleanText('shakespeare.txt', 'output.txt')

resultsBody = analyzeSource('output.txt', 28)

results = normalize2(normalize(resultsBody))

# Make the grid for output
nrows, ncols = len(results),26
image = np.zeros(nrows*ncols)

for m in range(len(results)):
	currentIndex= results[m]
	for n in range(len(currentIndex)):
		shade = currentIndex[n]*256
		image[m*26 + n] = 256-shade;

image = image.reshape((nrows, ncols))

# Labels
row_labels = range(1, nrows+1)
col_labels = charRange('A', 'Z')

plt.matshow(image, cmap=cm.YlGnBu)
plt.xticks(range(ncols), col_labels)
plt.yticks(range(nrows), row_labels)
#Workaround to turn the tick marks off
plt.tick_params(
    axis='both',        # changes apply to the x-axis
    which='both',       # both major and minor ticks are affected
    bottom='off',       # ticks along the bottom edge are off
    top='off',          # ticks along the top edge are off
	left='off',         # ticks along the left edge are off
	right='off',        # ticks along the right edge are off
    labelbottom='off')  # labels along the bottom edge are off

plt.suptitle("Letter Frequency by Index")
plt.savefig('output.png')
plt.show()


