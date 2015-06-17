import os 
import itertools

from awesome_print import ap 

DATA_BASEPATH = './data/twitter'
READ = 'r'
WRITE = 'w'
HEART_ATTACKS = 'heart_attack'

process_tweet_file = lambda filename: [line.split('|')[0] for line in open(filename,READ).read().splitlines()]

filenames = os.listdir(os.path.join(DATA_BASEPATH,HEART_ATTACKS))

text = itertools.chain.from_iterable(map(process_tweet_file,[os.path.join(DATA_BASEPATH,HEART_ATTACKS,filename) for filename in filenames]))


#ap(len(set(list(text))))

'''
     Number of tweets before deduplication: 16801
     Number of tweets after deduplication: 11989

'''

with open(os.path.join(DATA_BASEPATH,HEART_ATTACKS,'all-tweets.txt'),WRITE) as outfile:
	for tweet in text:
		print>>outfile,tweet
