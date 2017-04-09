import requests
import json

response = requests.get("https://api.nytimes.com/svc/topstories/v2/home.json", params=({'api-key': "1c643eb7e286434fab2b1ed00f495e89"}))

results = json.loads(response.content)['results']
##List containing dictionaries of title and abstracts of top articles in given subject 
articles = [{'Title':x['title'],'Abstract':x['abstract']} for x in results]
