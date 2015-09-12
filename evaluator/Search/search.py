import urllib2
import json
try:
    search_Term = "red beats by dr. dre headphones"
    search_Term = search_Term.replace(" ", "+")
    api_key = "3qukdf87ghrr2mf55rx9j2k8"
    url = "http://api.walmartlabs.com/v1/search?apiKey="+api_key
    query = url + "&query="+search_Term
    jsonText = urllib2.urlopen(query).read()
    results = json.loads(jsonText)
    for item in results['items']:
        print(item['name']+", "+"$"+str(item['salePrice']))
    input()
except Exception as e:
    print('Search Failed: '+str(e))
    input()
