import urllib2
import json
import xmltodict
import random


def define(query):
    """
    description: runs an api search on a word and returns the definition (there may be more than one)

    params: query, a string

    returns: a list of definitions
    """
    key = "f3815ee8-aa94-4c97-a283-fbf3cb5d2c05"
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=%s"
    url = url % (query, key)
    request = urllib2.urlopen(url)
    result = request.read()
    r = xmltodict.parse(result)
    out = json.loads(json.dumps(r))

    #print out["entry_list"]["entry"]["def"]["dt"]

    defs = []
    if isinstance(out["entry_list"]["entry"], list):
        for res in out["entry_list"]["entry"]:
            defs += get_def(res, query)
    elif isinstance(out["entry_list"]["entry"], dict):
        res = out["entry_list"]["entry"]
        defs = get_def(res, query)
    return defs


def get_def(res, query):
    """
    Description: Finds and returns the definition for a specific entry in the dictionary
    
    params: res, a dictionary of the form out["entry_list"]["entry"]
            query, the search query

    returns: a list of definitions
    """
    defs = []
    #print "Comparing '%r' with '%r'" % (query, str(res["@id"]))
    if len(res["@id"]) - len(query) <= 3:
        d = res["def"]["dt"]
        #print d
        for entry in d:
            #print entry
            if isinstance(entry, unicode) and is_legit_def(entry):
                defs.append(str(entry)[1:])
            elif isinstance(entry, dict):
                try:
                    if is_legit_def(entry["#text"]):
                        defs.append(str(entry["#text"])[1:])
                except:
                    pass
    return defs


def is_legit_def(string):
    """
    Description: Some tests for whether a string is a def because stupid api
    params: string, a string

    returns: a boolean
    """
    if len(string) > 3 and " " in string:
        return True
    else:
        return False

    
    
def get_pict(word):

    """
    description: run a word first through an api search function, then through an info function to get url of corresponding photo

    params: word, a string

    returns: url, a string
    """
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&format=json&nojsoncallback=1&media=photos&text=%s&sort=relevance&is_commons=true&extras=url_q"
    key = "e0e0c259e7e2a1f07f6c8e6a74579f12"
    url = url % (key, word)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)

    bound = 30
    if r["photos"]["total"] < bound:
        bound =  r["photos"]["total"]

    index = random.randrange(0, bound)
    
    return r["photos"]["photo"][index]["url_q"]
    

    
#takes: the search query
#replaces certain words with image urls
#returns: something
def pictify(query):
    d = define(query)



#Testing     
#print define("loquacious")

print get_pict("rose")

