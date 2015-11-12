import urllib2
import json
import xmltodict
import random


def get_stop_words():
    stop_words = []
    file = open("static/stop-word-list.csv", 'r')
    for line in file:
        stop_words += line.split(", ")
    file.close()
    return stop_words
    

def define(query):
    """
    description: runs an api search on a word and returns the definition (there may be more than one)

    params: query, a string

    returns: a list of definitions
    """
    
    q = query.replace(" ", "+")
    key = "f3815ee8-aa94-4c97-a283-fbf3cb5d2c05"
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=%s"
    url = url % (q, key)
    request = urllib2.urlopen(url)
    result = request.read()
    r = xmltodict.parse(result)
    out = json.loads(json.dumps(r))

    #print out["entry_list"]["entry"]["def"]["dt"]
    #print url
    #print out

    defs = []
    entries = out["entry_list"]["entry"]
    
    if isinstance(entries, list):
        for res in entries:
            defs += get_def(res, query)
    elif isinstance(entries, dict):
        defs = get_def(entries, query)
    return defs


def get_def(res, query):
    """
    Description: Finds and returns the definition for a specific entry in the dictionary
    
    params: res, a dictionary of the form out["entry_list"]["entry"]
            query, the search query

    returns: a list of definitions
    """
    defs = []
    if (query in res["@id"] and 
            len(res["@id"]) - len(query) <= 3 and 
            "def" in res):
        
        d = res["def"]["dt"]
        if isinstance(d, unicode):
            defs.append(str(d)[1:])
            return defs

        if ("#text" in d and
                isinstance(d["#text"], unicode) and
                is_legit_def(d["#text"], query)):
            defs.append(str(d["#text"])[1:])
            
        for entry in d:
            if (isinstance(entry, unicode) and
                        is_legit_def(entry, query)):
                defs.append(str(entry)[1:])
    
            if isinstance(entry, dict):
                try:
                    if is_legit_def(entry["#text"], query):
                        defs.append(str(entry["#text"])[1:])
                except:
                    pass
    return defs


def is_legit_def(definition, word):
    """
    Description: Some tests for whether a string is a def because stupid api
    params: def, a string
            word, a string

    returns: a boolean
    """
    if (len(definition) > 3 and
            " " in definition and
            len(definition) > len(word)):
        return True
    else:
        return False

    
    
def get_pict(word):
    """
    description: run a word through a picture search and return an image url

    params: word, a string

    returns: url, a string
    """
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&format=json&nojsoncallback=1&media=photos&text=%s&sort=relevance&extras=url_q"
    
    key = "e0e0c259e7e2a1f07f6c8e6a74579f12"
    url = url % (key, word)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)

    #bound = 30
    #if len(r["photos"]) < bound:
        #bound =  len(r["photos"]["total"])

    #index = random.randrange(0, bound)
    index = 0
    pic = word
    try:
        pic = r["photos"]["photo"][index]["url_q"]
    except:
        pass
    return pic 
    

    
#takes: the search query
#replaces certain words with image urls
#returns: something
def pictify(query):
    """  
    Description: replaces the words in the definition with image urls

    params: query, a string

    returns: a list of definitions with image urls
    """
    d = define(query)
    stop_words = get_stop_words()
    defs = []
    for definition in d:
        def_list = definition.split()
        words = []
        for word in def_list:
            if word not in stop_words:
                word = get_pict(word)
            words.append(word)
        defs.append(words)
    return defs



#Testing     
#print define("rose cut")
#print define("spontaneous combustion")
#print define("bug")
#print define("chicken")

#print get_pict("violent")
#print pictify("garrulous")

