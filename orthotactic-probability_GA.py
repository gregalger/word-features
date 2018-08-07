import sys
from collections import Counter
import math

print("Welcome to the Orthotactic Probability script!")

print("Enter the list of words in the target language, "+
		"each on a new line. When you are finished, "+
		"type Ctrl + D on a new line.")

data = sys.stdin.readlines()

words = []

for item in data:
	words.append(item.lower().strip())

print("\n")

n = len(max(words, key=len))

list_of_init1 = []
list_of_init2 = []
list_of_init3 = []
list_of_med2 = []
list_of_med3 = []
list_of_fin1 = []
list_of_fin2 = []
list_of_fin3 = []

for word in words:
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

init1_counts = Counter(list_of_init1)
init2_counts = Counter(list_of_init2)
init3_counts = Counter(list_of_init3)
med2_counts = Counter(list_of_med2)
med3_counts = Counter(list_of_med3)
fin1_counts = Counter(list_of_fin1)
fin2_counts = Counter(list_of_fin2)
fin3_counts = Counter(list_of_fin3)

init1_sum = len(list_of_init1)
init2_sum = len(list_of_init2)
init3_sum = len(list_of_init3)
med2_sum = len(list_of_med2)
med3_sum = len(list_of_med3)
fin1_sum = len(list_of_fin1)
fin2_sum = len(list_of_fin2)
fin3_sum = len(list_of_fin3)

init1_scores = {}
init2_scores = {}
init3_scores = {}
med2_scores = {}
med3_scores = {}
fin1_scores = {}
fin2_scores = {}
fin3_scores = {}

# ddbz stands for "don't divide by zero!!!"
def ddbz(counts, s, scores):
	for x in counts:
		if s > 1:
			scores[x] = math.log10(counts[x])/math.log10(s)
		else:
			scores[x] = 0.0

ddbz(init1_counts, init1_sum, init1_scores)
ddbz(init2_counts, init2_sum, init2_scores)
ddbz(init3_counts, init3_sum, init3_scores)
ddbz(med2_counts, med2_sum, med2_scores)
ddbz(med3_counts, med3_sum, med3_scores)
ddbz(fin1_counts, fin1_sum, fin1_scores)
ddbz(fin2_counts, fin2_sum, fin2_scores)
ddbz(fin3_counts, fin3_sum, fin3_scores)

print ("Enter the list of words whose orthotactic probability "+
		"you'd like to calculate, each on a new line. When you are finished, "+
		"type Ctrl + D on a new line.\n")

sys.stdin.seek(0)
data2 = sys.stdin.readlines()

words = []
for item in data2:
	words.append(item.lower().strip())

print("\n---\n")

# gdv stands for "get dictionary value" ...if the key exists!
def gdv(d, k):
	if d.get(k):
		return d[k]
	else:
		return 0.0

for word in words:
	word_score = []
	if len(word) == 1:
		word_score.append(gdv(init1_scores, word))
		word_score.append(gdv(fin1_scores, word))
	elif len(word) == 2:
		word_score.append(gdv(init1_scores, word[0]))
		word_score.append(gdv(fin1_scores, word[1]))
		word_score.append(gdv(init2_scores, word))
		word_score.append(gdv(fin2_scores, word))
	elif len(word) == 3:
		word_score.append(gdv(init1_scores, word[0]))
		word_score.append(gdv(init2_scores, word[0:2]))
		word_score.append(gdv(init3_scores, word))
		word_score.append(gdv(fin1_scores, word[-1]))
		word_score.append(gdv(fin2_scores, word[-2:]))
		word_score.append(gdv(fin3_scores, word))
	elif len(word) == 4:
		word_score.append(gdv(init1_scores, word[0]))
		word_score.append(gdv(init2_scores, word[0:2]))
		word_score.append(gdv(init3_scores, word[0:3]))
		word_score.append(gdv(med2_scores, word[1:3]))
		word_score.append(gdv(fin1_scores, word[-1]))
		word_score.append(gdv(fin2_scores, word[-2:]))
		word_score.append(gdv(fin3_scores, word[-3:]))
	elif len(word) == 5:
		word_score.append(gdv(init1_scores, word[0]))
		word_score.append(gdv(init2_scores, word[0:2]))
		word_score.append(gdv(init3_scores, word[0:3]))
		word_score.append(gdv(med2_scores, word[1:3]))
		word_score.append(gdv(med2_scores, word[2:4]))
		word_score.append(gdv(med3_scores, word[1:4]))
		word_score.append(gdv(fin1_scores, word[-1]))
		word_score.append(gdv(fin2_scores, word[-2:]))
		word_score.append(gdv(fin3_scores, word[-3:]))
	else:
		word_score.append(gdv(init1_scores, word[0]))
		word_score.append(gdv(init2_scores, word[0:2]))
		word_score.append(gdv(init3_scores, word[0:3]))
		word_score.append(gdv(fin1_scores, word[-1]))
		word_score.append(gdv(fin2_scores, word[-2:]))
		word_score.append(gdv(fin3_scores, word[-3:]))
		for x in range(len(word) - 3):
			word_score.append(gdv(med2_scores, word[x+1:x+3]))
		for x in range(len(word) - 4):
			word_score.append(gdv(med3_scores, word[x+1:x+4]))
	print word + "\t" + str(sum(word_score)/len(word_score))
