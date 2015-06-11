# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 11:38:12 2015

@author: Nik
"""

import sys, requests, codecs, json
from HTMLParser import HTMLParser
from jaccard import jaccard
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

idFirst = sys.argv[1]
idSecond = sys.argv[2]

parameters = {'format' : 'json', 'action' : 'query', 'revids' : idFirst, 'prop' : 'extracts', 'rvprop' : 'content', 'continue' : '', "exsectionformat" : "plain", "redirects" : ""}
parametersSecond = {'format' : 'json', 'action' : 'query', 'revids' : idSecond, 'prop' : 'extracts', 'rvprop' : 'content', 'continue' : '', "exsectionformat" : "plain", "redirects" : ""}

r = requests.get('http://en.wikipedia.org/w/api.php', params=parameters)
rSecond = requests.get('http://en.wikipedia.org/w/api.php', params=parametersSecond)

data = r.json()
dataSecond = rSecond.json()

def toPlainText(rdata, jsonFile, txtFile):
    with open(jsonFile, 'w') as outfile:
        json.dump(rdata, outfile)
    with codecs.open(txtFile, 'w', 'utf-8') as file2:
        ids = rdata['query']['pages'].keys()
        text = ' '.join([rdata['query']['pages'][idx]['extract'] for idx in ids])
        text = strip_tags(text)
        file2.write(text)

toPlainText(data, 'firstRev.json', 'firstRev.txt')
toPlainText(dataSecond, 'secondRev.json', 'secondRev.txt')

with open('jaccardData.txt', 'a') as outfile:
    print>>outfile,jaccard('firstRev.txt', 'secondRev.txt')
