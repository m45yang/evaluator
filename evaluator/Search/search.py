import urllib2
import json
import re

try:
    search_Term = "good day to die hard"
    query_search_Term = search_Term.replace(" ", "+")
    tokenized_Search_Term = search_Term.split(' ')
    api_key = "3qukdf87ghrr2mf55rx9j2k8"
    url = "http://api.walmartlabs.com/v1/search?apiKey="+api_key
    query = url + "&query="+query_search_Term
    jsonText = urllib2.urlopen(query).read()
    results = json.loads(jsonText)

    isExact = False
    #Clean String
    for item in results['items']:
        item['name'] = re.sub('\(.*?\)', '', item['name'])
        item['name'] = re.sub('[ \t]+$', '', item['name']).lower()
    #Check if an exact result exists for the given search query
    for item in results['items']:
        if(search_Term == item['name']):
            isExact = True
            print(item['name']+", "+"$"+str(item['salePrice']))
            break
    #if no exact results exist, just display all search results
    if not (isExact):
        for item in results['items']:
            tokenized_Item_Name = item['name'].split(' ')
            print(item['name']+", "+"$"+str(item['salePrice']))
    input()
except Exception as e:
    print('Search Failed: '+str(e))
    input()
