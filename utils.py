import urllib2, json


def define(query):

    """
    description: runs an api search on a word and returns the definition (there may be more than one)

    params: query, a string

    returns: definition, a list
    """
    
    url = "https://api.pearson.com:443/v2/dictionaries/ldoce5/entries?search=%s&headword=%s"
    url = url % (query, query)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)

    #how to get a single definition
    #print r
    #print r["results"][0]["senses"][0]["definition"][0]
    
    defs = []
    for res in r["results"]:
        if res["headword"] == query:
            try:
                defs.append(res["senses"][0]["definition"][0])
            except:
                pass
    print defs
    return defs


    
def get_pict(word):

    """
    description: run a word first through an api search function, then through an info function to get url of corresponding photo

    params: word, a string

    returns: url, a string
    """
    
    #searching for photo
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&format=json&media=photos&tags=%s&text=%s"
    key = "e0e0c259e7e2a1f07f6c8e6a74579f12"
    url = url % (key, word, word)

    photo_id = ""
    secret = ""
    
    #getting photo info (like url) by id
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=%s&photo_id=%s&secret=%s"
    url = url % (key, photo_id, secret)

    
#takes: the search query
#replaces certain words with image urls
#returns: something
def pictify(query):
    d = define(query)



#Testing     
define("stab")
define("eviscerate")
define("gallows")
