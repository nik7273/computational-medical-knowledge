from google import google

num_page = 3
'''
search_results = google.search("michael chary", num_page)


urls = [result.google_link for result in search_results]
with open('urltest','wb') as outfile:
  for url in urls:
    print>>outfile,url

'''
urls = open('urltest','rb').read().splitlines()    
print urls[0]

def extract_url(google_url):
  return google_url.split('?q=')[1].split('&sa')[0]

print extract_url(urls[0])