# -*- coding: utf-8 -*-

## Script to calculate the orthotactic probability of input words based
## on the distribution of letter sequences in any specified dictionary.
## The algorithm considers initial 1-, 2-, and 3-letter sequences, final
## 1-, 2-, and 3-letter sequences, and medial 2- and 3-letter sequences.
## It does not consider overall word length or ordinal position throughout
## the word.

## Imports
import sys
from collections import Counter
import math
import unicodecsv as csv
import os

## Necessary for encoding characters correctly in excel .csv, courtesy of StackOverflow
class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")
class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self
class UnicodeWriter:
	def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
		# Redirect output to a queue
		self.queue = StringIO.StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
		self.stream = f

		# Force BOM
		if encoding=="utf-16":
			import codecs
			f.write(codecs.BOM_UTF16)

		self.encoding = encoding
	def writerow(self, row):
		# Modified from original: now using unicode(s) to deal with e.g. ints
		self.writer.writerow([unicode(s).encode("utf-8") for s in row])
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		data = data.decode("utf-8")
		# ... and reencode it into the target encoding
		data = data.encode(self.encoding)

		# strip BOM
		if self.encoding == "utf-16":
			data = data[2:]

		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)
	def writerows(self, rows):
		for row in rows:
			self.writerow(row)

## File in current directory with list of words for which to calculate
## orthotactic probability. Each word should be listed on a new line
## in a plain text file titled "_input_words.txt".
with open("_input_words.txt", "r") as f:
	input_words = f.read().splitlines()

## File in the current directory with a dictionary of words against
## which to calculate orthotactic probability. Here, we use an English
## dictionary with 49,278 words.
with open("_english_dictionary_49278.txt", "r") as f:
	language_dictionary = f.read().splitlines()

language_words = []
for word in language_dictionary:
	language_words.append(word.lower().strip())

## Gather the lists of letter sequences of words in the language dictionary.
list_of_init1 = []
list_of_init2 = []
list_of_init3 = []
list_of_med2 = []
list_of_med3 = []
list_of_fin1 = []
list_of_fin2 = []
list_of_fin3 = []

for word in language_words:
	if len(word) == 1:
		list_of_init1.append(word)
		list_of_fin1.append(word)
	elif len(word) == 2:
		list_of_init1.append(word[0])
		list_of_init2.append(word)
		list_of_fin1.append(word[1])
		list_of_fin2.append(word)
	elif len(word) == 3:
		list_of_init1.append(word[0])
		list_of_init2.append(word[0:2])
		list_of_init3.append(word)
		list_of_fin1.append(word[-1])
		list_of_fin2.append(word[-2:])
		list_of_fin3.append(word)
	elif len(word) == 4:
		list_of_init1.append(word[0])
		list_of_init2.append(word[0:2])
		list_of_init3.append(word[0:3])
		list_of_med2.append(word[1:3])
		list_of_fin1.append(word[-1])
		list_of_fin2.append(word[-2:])
		list_of_fin3.append(word[-3:])
	elif len(word) == 5:
		list_of_init1.append(word[0])
		list_of_init2.append(word[0:2])
		list_of_init3.append(word[0:3])
		list_of_med2.append(word[1:3])
		list_of_med2.append(word[2:4])
		list_of_med3.append(word[1:4])
		list_of_fin1.append(word[-1])
		list_of_fin2.append(word[-2:])
		list_of_fin3.append(word[-3:])
	else:
		list_of_init1.append(word[0])
		list_of_init2.append(word[0:2])
		list_of_init3.append(word[0:3])
		list_of_fin1.append(word[-1])
		list_of_fin2.append(word[-2:])
		list_of_fin3.append(word[-3:])
		for x in range(len(word) - 3):
			list_of_med2.append(word[x+1:x+3])
		for x in range(len(word) - 4):
			list_of_med3.append(word[x+1:x+4])

## Count the letter sequences for each type. Keys are the letter sequence string,
## values are the counts.
init1_counts = Counter(list_of_init1)
init2_counts = Counter(list_of_init2)
init3_counts = Counter(list_of_init3)
med2_counts = Counter(list_of_med2)
med3_counts = Counter(list_of_med3)
fin1_counts = Counter(list_of_fin1)
fin2_counts = Counter(list_of_fin2)
fin3_counts = Counter(list_of_fin3)

## Count how many of each type of letter sequence.
init1_sum = len(list_of_init1)
init2_sum = len(list_of_init2)
init3_sum = len(list_of_init3)
med2_sum = len(list_of_med2)
med3_sum = len(list_of_med3)
fin1_sum = len(list_of_fin1)
fin2_sum = len(list_of_fin2)
fin3_sum = len(list_of_fin3)

## Create dictionaries for the probability of each letter sequence in each type.
## Keys are the letter sequence string, values are the probabilities.
init1_scores = {}
init2_scores = {}
init3_scores = {}
med2_scores = {}
med3_scores = {}
fin1_scores = {}
fin2_scores = {}
fin3_scores = {}

## Function to give a probability score for each letter sequence.
def probability_score(counts, sum, scores):
	for count in counts:
		# don't divide by zero
		if sum > 1:
			scores[count] = math.log10(counts[count])/math.log10(sum)
		else:
			scores[count] = 0.0

probability_score(init1_counts, init1_sum, init1_scores)
probability_score(init2_counts, init2_sum, init2_scores)
probability_score(init3_counts, init3_sum, init3_scores)
probability_score(med2_counts, med2_sum, med2_scores)
probability_score(med3_counts, med3_sum, med3_scores)
probability_score(fin1_counts, fin1_sum, fin1_scores)
probability_score(fin2_counts, fin2_sum, fin2_scores)
probability_score(fin3_counts, fin3_sum, fin3_scores)

## Function to get the value for key in dictionary, or return 0.0.
## Necessary because some letter sequences in the input words
## may not exist in the dictionary.
def get_value(dict, key):
	if dict.get(key):
		return dict[key]
	else:
		return 0.0

## Create a list of lists to hold the input words and their probability scores.
words_and_scores = []

## Create a probability score for each input word. The score is the average of the
## probability of each letter sequence calculated.
for word in input_words:
	word_score = []
	if len(word) == 1:
		word_score.append(get_value(init1_scores, word))
		word_score.append(get_value(fin1_scores, word))
	elif len(word) == 2:
		word_score.append(get_value(init1_scores, word[0]))
		word_score.append(get_value(fin1_scores, word[1]))
		word_score.append(get_value(init2_scores, word))
		word_score.append(get_value(fin2_scores, word))
	elif len(word) == 3:
		word_score.append(get_value(init1_scores, word[0]))
		word_score.append(get_value(init2_scores, word[0:2]))
		word_score.append(get_value(init3_scores, word))
		word_score.append(get_value(fin1_scores, word[-1]))
		word_score.append(get_value(fin2_scores, word[-2:]))
		word_score.append(get_value(fin3_scores, word))
	elif len(word) == 4:
		word_score.append(get_value(init1_scores, word[0]))
		word_score.append(get_value(init2_scores, word[0:2]))
		word_score.append(get_value(init3_scores, word[0:3]))
		word_score.append(get_value(med2_scores, word[1:3]))
		word_score.append(get_value(fin1_scores, word[-1]))
		word_score.append(get_value(fin2_scores, word[-2:]))
		word_score.append(get_value(fin3_scores, word[-3:]))
	elif len(word) == 5:
		word_score.append(get_value(init1_scores, word[0]))
		word_score.append(get_value(init2_scores, word[0:2]))
		word_score.append(get_value(init3_scores, word[0:3]))
		word_score.append(get_value(med2_scores, word[1:3]))
		word_score.append(get_value(med2_scores, word[2:4]))
		word_score.append(get_value(med3_scores, word[1:4]))
		word_score.append(get_value(fin1_scores, word[-1]))
		word_score.append(get_value(fin2_scores, word[-2:]))
		word_score.append(get_value(fin3_scores, word[-3:]))
	else:
		word_score.append(get_value(init1_scores, word[0]))
		word_score.append(get_value(init2_scores, word[0:2]))
		word_score.append(get_value(init3_scores, word[0:3]))
		word_score.append(get_value(fin1_scores, word[-1]))
		word_score.append(get_value(fin2_scores, word[-2:]))
		word_score.append(get_value(fin3_scores, word[-3:]))
		for x in range(len(word) - 3):
			word_score.append(get_value(med2_scores, word[x+1:x+3]))
		for x in range(len(word) - 4):
			word_score.append(get_value(med3_scores, word[x+1:x+4]))
	words_and_scores.append([word, sum(word_score)/len(word_score)])

## Write output to documents.

# write temp document
with open("/tmp/temp-orthotactic-probability-results.csv", "w") as f:
	writer = csv.writer(f)
	writer.writerow(["Word", "Probability Score"])
	writer.writerows(words_and_scores)

# import some more stuff here to deal with encoding issues for .csv file
import csv, codecs, StringIO

# write permanent document from referenced temp document
dir = os.getcwd()
f = dir + "/orthotactic-probability-results.csv"
with open("/tmp/temp-orthotactic-probability-results.csv", 'rb') as fin, open(f, 'wb') as fout:
	reader = UnicodeReader(fin)
	writer = UnicodeWriter(fout, quoting=csv.QUOTE_ALL)
	for line in reader:
		writer.writerow(line)
