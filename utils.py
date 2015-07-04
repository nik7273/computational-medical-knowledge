import nltk
import string
import itertools 

import numpy as np 

from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

lmtzr = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))
def is_reference_number(aStr):
	return all([ch.isdigit() or ch in string.punctuation for ch in aStr])

def cleanse(text):
	tokens = [lmtzr.lemmatize(token.lower()) for token in  word_tokenize(text) 
				if token not in string.punctuation 
					 and not token.isdigit() 
					 and len(token) >2
					 and not token.endswith('-')
					 and not is_reference_number(token)]
	tokens = set(tokens) - stopwords
	return tokens
 
format = lambda aStr: r'\Large \textbf{\textsc{%s}}'%aStr

def adjust_spines(ax,spines=['bottom','left']):
	for loc, spine in ax.spines.iteritems():
		if loc in spines:
			spine.set_position(('outward',10))
			#spine.set_smart_bounds(True) #Doesn't work for log log plots
			spine.set_linewidth(1)
		else:
			spine.set_color('none') 
	if 'left' in spines:
		ax.yaxis.set_ticks_position('left')
	else:
		ax.yaxis.set_ticks([])

	if 'bottom' in spines:
		ax.xaxis.set_ticks_position('bottom')
	else:
		ax.xaxis.set_ticks([])

def jaccard(one,two):
	#TODO: Generalize to N-inputs
	one = set(one) if type(one) != type(set) else one
	two = set(two) if type(two) != type(set) else two 

	if len(one | two ) == 0:
		return 0
	else:	
		return len(one & two)/float(len(one | two))

def resample(amalgamated_corpora,n_partitions,partition_sizes = None,repetitions=3, save=False,monitor=False): 
	sample_size = sum(partition_sizes)
	if not type(amalgamated_corpora) == type(list):
		amalgamated_corpora = amalgamated_corpora.split()
	
	resampled_values = np.zeros((repetitions,3))

	for j in xrange(repetitions):
		if monitor:
			if j%100==0:
				print j
		new_documents = [np.random.choice(amalgamated_corpora,partition_sizes[i]) for i in xrange(n_partitions)]
		for one, two in itertools.combinations(xrange(n_partitions),2):
			 resampled_values[j,:] = jaccard(new_documents[one],new_documents[two])
	if save:
		np.savetxt('resampled-jaccard-distributions.csv',resampled_values.flatten(),delimiter='\t')
			
	return resampled_values.flatten()