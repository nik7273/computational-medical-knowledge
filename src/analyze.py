# -*- coding: utf-8 -*-
"""

	python analyze.py --pipeline "method1 method2" --input "file1 file2"

"""

import optparse
import itertools
import os 
import matplotlib
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt 
import utils as tech
import numpy as np 

from sys import argv
from os.path import basename 


parser = optparse.OptionParser()
parser.add_option('--pipeline', action="store", default="jaccard", help="List of steps in pipeline")
parser.add_option('--input', action="store", default=".", help="List of input files")
options, args = parser.parse_args()

command_line_arguments = [command.strip().lower() for command in options.pipeline.split()]
pipeline = [getattr(tech, command) for command in command_line_arguments]

if os.path.isdir(options.input):
	input_filenames = [os.path.join(options.input,filename.strip().lower()) for filename in os.listdir(options.input)]
	input_filenames = [filename for filename in input_filenames if filename.endswith('.txt')]
else:
	input_filenames  = [filename.strip().lower() for filename in options.input.split()]
data = {basename(filename):tech.filestream_to_word_list(open(filename,'rb')) for filename in input_filenames}
#Analysis methods are pairwise

#Calculate Jaccard similarity

keys = data.keys()
jaccard_similarity = np.zeros((len(keys),len(keys)))
for j in xrange(jaccard_similarity.shape[1]):
	for i in xrange(j):
		jaccard_similarity[i,j] = tech.jaccard(data[keys[i]],data[keys[j]])

jaccard_similarity += jaccard_similarity.transpose()
jaccard_similarity[np.diag_indices_from(jaccard_similarity)] = 1

np.savetxt('../data/jaccard_similarity.tsv',jaccard_similarity,fmt='%.04f',header = ' '.join(keys))

fig, ax  = plt.subplots()
ax = sns.heatmap(jaccard_similarity, annot=True, fmt='.02f', square = True,
					  xticklabels = keys, yticklabels=keys)
plt.tight_layout()
plt.savefig('../graphs/jaccard_similarity.png')