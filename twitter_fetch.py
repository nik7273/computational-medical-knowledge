import json,os,twitter, dropbox, gzip

from datetime import datetime
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pprint import pprint
from optparse import OptionParser
from progress.bar import Bar

"""
    
    Example call:
        python twitter_fetch.py --t keys.json --k "heart attack_palpitations" --o "../data/twitter" --m 1000000

"""

#--Load input from command line
op = OptionParser()
op.add_option('--t', dest='keys', type='str', help='Path of key files')
op.add_option('--k', dest='keywords',type='str',help='Path of keywords')
op.add_option('--o',type="str", dest="outpath")
op.add_option('--m',type='int',dest="MAX_NUMBER_OF_TWEETS",default=100)
op.print_help()

opts,args = op.parse_args()
if len(args) > 0:
    op.error('This script only takes arguments preceded by command line options.')

if not opts.outpath:
    opts.corpus = os.getcwd()
    print 'No output path specified. Using current working directory.'

search_terms = opts.keywords.split('_')

if not os.path.exists(opts.outpath):
    os.makedirs(opts.outpath)
    
for search_term in search_terms:
    if not os.path.isdir(os.path.join(opts.outpath,search_term)):
        os.makedirs(os.path.join(opts.outpath,search_term))

if not opts.keys:
    opts.keys = json.load(open('../../data/keys.json','rb'))
    print 'No access token specified. Searching for default tokens'
else:     
    opts.keys = json.load(open(opts.keys,'rb'))


client= dropbox.client.DropboxClient(opts.keys['dropbox']['access_token'])
class listener(StreamListener):
    
    def __init__(self, api=None, path=None,outname='output',MAX_NUMBER_OF_TWEETS=100,TWEETS_PER_FILE=10,progress_bar=None):
        #I don't remember exactly why I defined this.
        self.api = api

        #We'll need this later.
        self.path = path
        self.count = 0
        self.outname = outname 
        self.progress_bar = progress_bar
        self.MAX_NUMBER_OF_TWEETS = MAX_NUMBER_OF_TWEETS
        self.TWEETS_PER_FILE = TWEETS_PER_FILE

    def on_data(self, data):
        all_data = json.loads(data)       
        tweet_text = ' '.join(word for word in all_data["text"].split() if all(ord(ch)<128 for ch in word))     
        tweet_id = all_data["id"]
        filename = os.path.join(self.path,'%s_%s.txt'%(self.outname,datetime.now().strftime('%Y-%m-%d-%H')))
        with open(filename,"a") as fid: #This open and closes the same file a lot of times. Hack for now. 
            print>>fid, ' %s | %s'%(tweet_text,tweet_id)
            self.count += 1 
            if self.progress_bar:
                self.progress_bar.next()

        if self.count < self.MAX_NUMBER_OF_TWEETS:
            return True
        else:
            if self.progress_bar:
                self.progress_bar.finish()
            return False

    def on_error(self, status):
        return True #I believe this functions like pass in a try-except blocks

    def on_timeout(self):
        return True # Don't kill the stream

auth = OAuthHandler(opts.keys['twitter']['consumer_key'], opts.keys['twitter']['consumer_secret'])
auth.set_access_token(opts.keys['twitter']['access_token'],opts.keys['twitter']['access_token_secret'])

TWEETS_PER_FILE = 10000
'''
bar = Bar('Acquiring control tweets', max=opts.MAX_NUMBER_OF_TWEETS)
control_stream = twitter.TwitterStream(
    auth=twitter.OAuth(opts.keys['twitter']['access_token'], opts.keys['twitter']['access_token_secret'], 
        opts.keys['twitter']['consumer_key'], opts.keys['twitter']['consumer_secret']), timeout=False, heartbeat_timeout=1000000)
iterator = control_stream.statuses.sample()
counter = 0

for tweet in iterator:
    filename = os.path.join(control_path,'control_%d'%(counter/TWEETS_PER_FILE))
    with gzip.open(filename,'a') as fid:
        print>>fid,tweet
        counter += 1
        bar.next()
    if counter > opts.MAX_NUMBER_OF_TWEETS:
        break
bar.finish()
'''

for search_term in search_terms:
    bar = Bar('Acquiring tweets mentioning %s'%search_term, max=opts.MAX_NUMBER_OF_TWEETS)
    try:
        caseStream = Stream(auth, listener(path=os.path.join(opts.outpath,search_term),
                outname=search_term, MAX_NUMBER_OF_TWEETS=opts.MAX_NUMBER_OF_TWEETS,TWEETS_PER_FILE=TWEETS_PER_FILE,
                progress_bar = bar)) 
        caseStream.filter(track=search_terms)
    except Exception as e:
        print e
