# -*- coding: utf-8 -*-

#GET JACCARD SIMILARITY OF ALL HEART RELATED ARTICLES ON WIKIPEDIA (BETWEEN THEMSELVES)

from utils import jaccard
import wikipedia, codecs, nltk
from findRelevantArticles import findRelevantArticles
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import subprocess as sub #Running BASH script within python???
import matplotlib.pyplot as plt
import numpy as np

lemma = nltk.WordNetLemmatizer()
relArticles = findRelevantArticles("Heart Attack")
articlefilelist = []
wordslist = ['../STEMI_words','../NSTEMI_words','../WIKI_words']

for article in relArticles:
    articlefilename = "content_"+str(article)+".txt"
    with codecs.open(articlefilename,'wb', 'utf-8') as outfile:
        content = wikipedia.page(article).content
        content = [lemma.lemmatize(word) for word in content]
        content = set(content)
        for word in content:
            print>>outfile,word
    articlefilelist.append(articlefilename)

for piece in wordslist:
    articlefilelist.append(piece)

matrix = np.matrix([[jaccard(i,j) for i in articlefilelist] for j in articlefilelist])
print matrix

with open('jaccardVals', 'wb') as outfile:
    print>>outfile,matrix
    