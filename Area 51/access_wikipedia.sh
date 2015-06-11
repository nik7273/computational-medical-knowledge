#!/bin/bash
curl --globoff --get 'http://en.wikipedia.org/w/api.php' --data-urlencode format="json"" --data-urlencode action="query" --data-urlencode titles="Animal" --data-urlencode prop="extracts" --data-urlencode rvprop="content" --data-urlencode continue="" --data-urlencode exsectionformat="plain" > htmldata.txt 2>/dev/null
cat htmldata.txt | sed 's|<[^>]*>||g' > stripdata.txt
# In the above curl query, the parameter "title" is passed with Animal as its value.
# I mean to make this into a command line option so any article can be accessed.
# line 3 uses sed to strip html tags from the output file (htmldata.txt) so the plaintext is printed.
# Error in this file is that JSON still exists in "stripdata.txt"
