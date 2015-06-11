# -*- coding: utf-8 -*-
"Get frequencies and plot them"
from pdfParser import pdfparser
import nltk, matplotlib, numpy, pylab, string, codecs
from plotSave import plot_and_save
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop = stopwords.words('english')
READ = 'rb'
WRITE = 'wb'
lemma = nltk.WordNetLemmatizer()
punkt = set(string.punctuation)
d={}
with open("abbreviation_reference.txt",READ) as f:
    d = dict(x.split(' ') for x in f)
measures = ['cm', 'in', 'mg', 'lb', 'kg', 'mm', 'ft']


def fromPDFtoText(infile, outfile):
    if ".pdf" in infile:
        with codecs.open(outfile,WRITE,'utf-8') as outfile:
            print>>outfile,pdfparser(infile)
        return outfile
    else:
        return infile



def getAndListFreqs(textfile, wordsFile, listFile):
    #gets frequencies of words and lists them in outer file
    data = [word.lower() for word in word_tokenize(codecs.open(textfile,READ,'utf-8').read()) if word not in punkt]
    for item in data:
        if item in d.keys():
            data[data.index(item)] = d[item]
            item.replace("_"," ")
            word_tokenize(item)
    data = [lemma.lemmatize(word) for word in data]
    data = [word for word in data if word not in stop]
    data = [word for word in data if word not in measures]
    with codecs.open(wordsFile,WRITE,'utf-8') as outfile:
        for word in data:
            print>>outfile,word
    distribution = nltk.FreqDist(codecs.open(wordsFile, READ).read().splitlines())
    commonWord = distribution.most_common(30)
    words,freqs = zip(*commonWord)
    with codecs.open(listFile,WRITE,'utf-8') as outfile:
        for x,y in commonWord:
            print>>outfile, "%s %s" % (y, x)
    return {"words": words, "freqs": freqs}


