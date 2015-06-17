import os 
import itertools

from awesome_print import ap 

DATA_SAVEPATH = './data/twitter'
DATA_SOURCEPATH = './data_sources/twitter'
READ = 'r'
WRITE = 'w'
HEART_ATTACKS = 'heart_attack'
PALPITATIONS = 'palpitations'
process_tweet_file = lambda filename: [line.split('|')[0] for line in open(filename,READ).read().splitlines()]

filenames = os.listdir(os.path.join(DATA_SOURCEPATH,HEART_ATTACKS))
filenames = [filename for filename in filenames if not os.path.isdir(filename) and filename.endswith('.txt')]

text = itertools.chain.from_iterable(map(process_tweet_file,[os.path.join(DATA_SOURCEPATH,HEART_ATTACKS,filename) 
				for filename in filenames]))

#ap(len(set(list(text))))

'''
     Number of tweets before deduplication: 16801
     Number of tweets after deduplication: 11989

'''

with open(os.path.join(DATA_SAVEPATH,HEART_ATTACKS,'all-tweets.txt'),WRITE) as outfile:
	for tweet in text:
		print>>outfile,tweet
