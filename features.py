import re
import nltk
import string
from nltk.util import ngrams
from nltk import FreqDist
from collections import Counter

def detect_yeah(row, feature):
	regex = re.compile('[^a-zA-Z]')
	word = regex.sub('', row.split(' ', 1)[0]).lower()
	if(word == "yeah"):
		feature.append(1)
	else:
		feature.append(0)

def detect_prop(row):
	regex = re.compile('[^a-zA-Z]')
	word = regex.sub('', row.split(' ', 1)[0]).lower()
	if(word == "i" or word == "im" or word == "you" or word == "youre"):
		return 1
	else:
		return 0

def get_uni(first, second, uni):
	bigramfdist = FreqDist()
	for line in first:
		token = nltk.word_tokenize(line)
		token = [x for x in token if not re.fullmatch('[' + string.punctuation + ']+', x)]
		bigrams = ngrams(token, 1)
		bigramfdist.update(bigrams)
	
	print(bigramfdist.most_common(50))
	print(bigramfdist.get("but"))
	
	# print(bigramfdist.viewitems())


	# regex = re.compile('[^a-zA-Z]')
	# for line in first:
	# 	for word in line.split():
	# 		word = regex.sub('', word).lower()
	# 		if(uni.get(word) == None):
	# 			uni[word] = 1
	# 		else:
	# 			uni[word] += 1

	# for line in second:
	# 	for word in line.split():
	# 		word = regex.sub('', word).lower()
	# 		if(uni.get(word) == None):
	# 			uni[word] = 1
	# 		else:
	# 			uni[word] += 1

	# for key, value in dict(uni).items():
	# 	if value < 5000:
	# 		del uni[key]

	# for key in uni:
	# 	print(key)
	# print(uni)
	# print(len(uni))

def uni_feature(row, uni, feature):
	id = 0
	uni_temp = {}
	for key in uni:
		uni_temp[key] = id
		id += 1

	buckets = [0] * len(uni_temp)

	regex = re.compile('[^a-zA-Z]')
	for word in row.split():
		word = regex.sub('', word).lower()
		# print(uni_temp.get(word))
		if(uni.get(word) != None):
			buckets[uni_temp.get(word)] += 1

	for item in buckets:
		feature.append(item)


		