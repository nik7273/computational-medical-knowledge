#!/usr/local/bin/python
import os
import json
import re 
import cPickle

import numpy as np
import utils as tech

import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['text.usetex'] = True

READ = 'r'
WRITE = 'w'
base = os.path.join(os.getcwd(),'data')
sources = ['harrison','wikipedia','braunwald']
keywords = [word.replace(' ','_') for word in open('keywords').read().splitlines()]
CORPUS_FILENAME = 'corpus.json'

'''
    Data files structured as:

     	./data/source/keyword 
'''

#---LOAD DATA
if not os.path.isfile(CORPUS_FILENAME):
	#More expressive than itertools.product, small loops --> no important speed or memory difference
	corpus = {}
	for source in sources:
		corpus[source] = {}
		for disease in keywords:
			path = os.path.join(base,source,disease)
			text = ' '.join(open(os.path.join(path,filename),READ).read() for filename in os.listdir(path))
			text = text.replace('.',' ').replace("\n"," ")
			text = re.sub(r"[^\x00-\x7F]","",text) #Regexp faster than iterating through string to remove non-ASCII
			corpus[source][disease]  = list(tech.cleanse(text)) 
			#Cleanse returns type set. Type set is not JSON serializable. Type list is.
	json.dump(corpus,open(CORPUS_FILENAME,WRITE))

else:
	corpus = json.load(open(CORPUS_FILENAME,READ))


#--- CALCULATE JACCARD SIMILARITY

source_rubric = [[source for source in sources] 
						 for source in sources]


filenames = ['jaccard-similarity-%s'%disease for disease in keywords]
filenames += ['jaccard-similarities.json']


if not all([os.path.isfile(filename) for filename in filenames]):
	jaccard_matrices = {disease:np.zeros((len(sources),len(sources))) for disease in keywords}
	for disease in keywords:
		jaccard_matrices[disease] = np.array([[tech.jaccard(corpus[sources[i]][disease],corpus[sources[j]][disease])
											for i in xrange(len(sources))]
											for j in xrange(len(sources))])


		fig = plt.figure()
		ax = fig.add_subplot(111)
		cax = ax.imshow(jaccard_matrices[disease],interpolation='nearest',aspect='equal',vmin=0,vmax=1)

		ax.set_xticks(range(len(sources)))
		ax.set_yticks(range(len(sources)))

		ax.set_xticklabels(map(tech.format,sources))
		ax.set_yticklabels(map(tech.format,sources))
		cbar = plt.colorbar(cax)
		cbar.set_label(tech.format('Jaccard Similarity'))
		fig.tight_layout()
		plt.savefig('jaccard-similarity-%s'%disease)

	cPickle.dump(jaccard_matrices,open('jaccard-similarities.json',WRITE))

#--- BOOTSTRAPPING
lens = [len(corpus[source][disease]) for source in sources] #Does order matter?
amalgamated_corpus = ' '.join(' '.join(corpus[source][disease]) for disease in keywords for source in sources)
#N.B. Don't depucliated -- must preserve original word frequencies for resampling
jaccard_distributions = tech.resample(amalgamated_corpus,n_partitions=len(lens),partition_sizes=lens,repetitions=10000,
	monitor=True,save=True)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(jaccard_distributions,color='k')
tech.adjust_spines(ax)
ax.set_xlabel(tech.format('Jaccard Similarity'))
ax.set_ylabel(tech.format('No. of occurence'))
plt.tight_layout()
plt.savefig('distribution-jaccard-similarities.tiff')

