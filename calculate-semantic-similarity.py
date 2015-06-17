import nltk
import json
import itertools

import numpy as np 

from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet
brown_ic = wordnet_ic.ic('ic-brown.dat')

corpus = json.load(open('corpus.json','r'))

sources = ['harrison','wikipedia','braunwald','twitter']
keywords = [word.replace(' ','_') for word in open('keywords').read().splitlines()]

all_words = {disease:[] for disease in keywords}

'''
harrison heart_attack 2592
wikipedia heart_attack 1737
braunwald heart_attack 8188
twitter heart_attack 19018
harrison palpitations 301
wikipedia palpitations 1127
braunwald palpitations 8083
twitter palpitations 717
'''

for disease in keywords:
	#for source in sources:
	#	print '%s %s %d'%(source,disease,len(corpus[source][disease]))
	all_words[disease] = itertools.chain.from_iterable(corpus[source][disease] for source in sources)

#Look at semantic similarity and membership

'''
	Length before deduplication
	heart_attack 31535
	palpitations 10228

	Length after deduplication
	heart_attack 26268
	palpitations 9115

'''

#for disease in keywords:
	#print '%s %d'%(disease,len(set(list(all_words[disease]))))

semantic_similarities = {}

for disease in keywords:
	print 

'''
for disease in keywords:
	semantic_similarities[disease] = np.zeros((len(all_words[disease]),len(all_words[disease])))
	for i in xrange(len(all_words[disease])):
		for j in xrange(i):
			semantic_similarities[i,j] = 

'''