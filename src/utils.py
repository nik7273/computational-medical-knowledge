# -*- coding: utf-8 -*-
#UTILITIES
import nltk
import string

from nltk.collocations import *
from nltk.corpus import stopwords

def bigramFinder(FileA):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    with open(FileA,'rb') as infile:
        finder = BigramCollocationFinder.from_words(nltk.word_tokenize(infile.read()))  
    bigrams = finder.nbest(bigram_measures.pmi, 20)
    return bigrams

'''
def jaccard(file1, file2):
    lst1 = set(open(file1,'rb').read().splitlines())
    lst2 = set(open(file2,'rb').read().splitlines())
    return float(len(lst1 & lst2))/len(lst1 | lst2)
'''

def jaccard(lst1,lst2):
	lst1 = set(lst1)
	lst2 = set(lst2)
	return len(lst1 & lst2)/float(len(lst1 | lst2))

def filestream_to_word_list(fstream, lemmatize=True, remove_stopwords=True):
	''' TODO: Increase stopword coverages '''
	text = fstream.read().splitlines()
	text = [''.join(ch for ch in line.strip() if ord(ch)<128) for line in text]
	text = [line.lower() for line in text if line != '']
	if remove_stopwords:
		text = [word for word in nltk.word_tokenize(' '.join(text)) if word not in stopwords.words('english')]
		text = [word for word in text if word not in set(string.punctuation) and not word.isdigit()]
	return set(text)