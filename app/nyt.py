import requests
import json

NYT_KEY = json.loads(open('app/.NYT_KEY.json').read())['API_KEY']

def news():
    response = requests.get("https://api.nytimes.com/svc/topstories/v2/home.json", params=({'api-key': NYT_KEY }))

    results = json.loads(response.content)['results']
    ##List containing dictionaries of title and abstracts of top articles in given subject
    # toparticles = [{'Title':x['title'],'Abstract':x['abstract']} for x in results][:3]
    toparticles = [{'Abstract':x['abstract']} for x in results][:3]
    output = ""
    for i in range(3):
        modifiedString = toparticles[i]['Abstract'].encode("utf-8")
        output += str(modifiedString) + "\n"
    return(output)
