cat "$1" | jq '.[] | .id ' | while read id
do
	cat "$1" | jq '.[] | ."caption-id" ' | while read captid
	do	
		python yt_fetch_captions.py --videoid=$line --action='download' --captionid=$captid
	done

done