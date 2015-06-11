import json 
import gzip
import os 

from awesome_print import ap 

cwd = './data/twitter/heart attack'
READ = 'rb'
WRITE = 'wb'
filenames = [filename for filename in os.listdir(cwd) if filename.endswith('gzip')]
for filename in filenames:
	full_filename = os.path.join(cwd,filename)
	with gzip.open(full_filename,'rb') as in_file, open(full_filename.replace('gzip','txt'),'wb') as outfile:
		json_file = json.loads(in_file.read().decode(''))
			