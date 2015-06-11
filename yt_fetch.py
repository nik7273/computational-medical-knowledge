import os 
import json 

from YouTubeSearch import YouTubeSearch
from awesome_print import ap 

keywords = open('keywords').read().splitlines()
WRITE = 'wb'
for keyword in keywords:
    record = []
    with open(os.path.join(os.getcwd(),'./data/youtube/%s'%keyword),'a') as outfile:
        query = YouTubeSearch(keyword)
        for video in query:
            print>>outfile,' '.join(video['comments'])
            record.append(video)
    json.dump(record,open(os.path.join(os.getcwd(),'data','youtube','%s.json'%keyword),'wb'))