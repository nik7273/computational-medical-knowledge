from googleapiclient.discovery import build 

from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import json
import urllib
import sys 

class YouTubeSearch(object):
	def __init__(self, term):

		self.term = term
		self.keywords = ['medical','medicine','science','scientific','coronary','cardiac','body','animation',
							'heart-attack','paramedics','911','rescue','physician','death','rhythm','symptoms','signs',
							'irregular']

		self.developer_key = "AIzaSyAe-JITdHfLxq7wH3j0xxCw8EzlVIY2CZI"
		self.api_service_name = "youtube"
		self.api_version = "v3"
		self.read_write_ssl_scope = "https://www.googleapis.com/auth/youtube.force-ssl"


		self.client_secrets_file = "client_secret_key.json"
		self.youtube = build(self.api_service_name, self.api_version,
				developerKey=self.developer_key)

		self.videos = []
		self.search()


	def search(self):
		#Still have to deal with pagination!, pass tokens, check for end of video
		self.search_response = self.youtube.search().list(q=self.term,part="id,snippet",maxResults=50).execute()

		for search_result in self.search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video" :
				if any([keyword in search_result['snippet']['description'].lower() for keyword in self.keywords]):

					caption_handles = self.youtube.captions().list(part='snippet',videoId=search_result['id']['videoId']).execute()
          
					if len(caption_handles['items'])>0:
						caption_id = caption_handles['items'][0]['id']

				
					comments = self.youtube.commentThreads().list(part="snippet",videoId = search_result["id"]["videoId"],
													 textFormat="plainText").execute()
	
					filtered_comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'].encode('ascii','ignore')
										 for item in comments['items']]

					filtered_comments = [comment for comment in filtered_comments if comment != '']

					self.videos.append({"title":search_result["snippet"]["title"],
							"id":search_result["id"]["videoId"], "comments":filtered_comments,
							'caption-id':caption_id})

	def __iter__(self):
		for item in self.videos:
			yield item