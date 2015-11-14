import urllib2
import json
import xmltodict
import random

stop_words = []

def get_stop_words():
    """
    reads stop-words into dictionary from static
    """
    global stop_words
    file = open("static/stop.csv", 'r')
    append = stop_words.append
    for line in file:
        append(line.strip())
    file.close()
    

def define(query):
    """
    Runs an api search on a word and returns the definition(s) of the word

    params: query, a string

    returns: a dictionary of definitions

    key: "definitions"     value: a list of definitions
    key: "suggestions"     value: a list of suggestions if no matches are found     """    
    q = query.replace(" ", "+")
    key = "f3815ee8-aa94-4c97-a283-fbf3cb5d2c05"
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=%s"
    url = url % (q, key)
    request = urllib2.urlopen(url)
    result = request.read()

    result = remove_stupid_tags(result)
    r = xmltodict.parse(result)
    out = json.loads(json.dumps(r))

    defs = []
    retval = {}

    if "suggestion" in out["entry_list"]:
        defs = get_suggestions(out["entry_list"])
        retval["suggestions"] = defs 
    else:
        entries = out["entry_list"]["entry"]
        if isinstance(entries, list):
            for res in entries:
                defs += get_def(res, query)
        elif isinstance(entries, dict):
            defs = get_def(entries, query)
        retval["definitions"] = defs
    return retval
    

def remove_stupid_tags(text):
    """
    Primes the text xml by removing unecessary tags and returns a cleaner version of it as a string  
    """
    tags = ["<it>", "</it>", "<d_link", "</d_link>",
            "<sx>", "</sx>", "<cat>", "</cat>",
            "<ca>", "</ca>", "<vi>" , "</vi>"]
    new = text
    for tag in tags:
        new = new.replace(tag, "")
    return new
    

def get_suggestions(d):
    """
    Extracts the suggestions out of dictionary d and returns them in a list
    """
    sugg = []
    if isinstance(d["suggestion"], unicode):
        sugg[0] = d["suggestion"]
    elif isinstance(d["suggestion"], list):
        for word in d["suggestion"]:
            sugg.append(str(word))
    return sugg
    


def get_def(res, query):
    """
    Finds and returns the definition for a specific entry in the dictionary
    
    params: res, a dictionary of the form out["entry_list"]["entry"]
            query, the search query

    returns: a list of definitions
    """
    defs = []
    d_append = defs.append
    if (query in res["@id"] and 
            len(res["@id"]) - len(query) <= 3 and 
            "def" in res):
        d = res["def"]["dt"]
        
        if isinstance(d, unicode):
            d_append(str(d)[1:])
            return defs

        for entry in d:
            if (isinstance(d, list) and
                    isinstance(entry, unicode)):
                d_append(str(entry)[1:])

            elif (isinstance(d, dict)):
                 if (isinstance(d[entry], unicode) and
                         is_legit_def(d[entry], query)):
                     d_append(str(d[entry])[1:])
                
                 elif ("#text" in d[entry] and
                         is_legit_def(d[entry]["#text"], query)):
                     d_append(str(d[entry]["#text"])[1:])
                
    return defs


def is_legit_def(definition, word):
    """
    Tests whether the string definition is legit based on length compared to original search query word and whether def is more than one word long
    Returns True if legit
    """  
    if (len(definition) > 3 and
            " " in definition and
            len(definition) > len(word)):
        return True
    else:
        return False

    
    
def get_pict(word):
    """
    Runs a word through a picture search and returns an image url as a string
    """
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&format=json&nojsoncallback=1&media=photos&text=%s&sort=relevance&extras=url_q"
    key = "e0e0c259e7e2a1f07f6c8e6a74579f12"
    url = url % (key, word)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)

    #bound =  len(r["photos"]["total"])

    #index = random.randrange(0, bound)
    index = 0
    pic = word
    try:
        pic = r["photos"]["photo"][index]["url_q"]
    except:
        pass
    return pic 
    

    

def pictify(d):
    """  
    Replaces the words in the definition with image urls

    params: d, a dictionary of definitions or suggestions

    returns: a dictionary of definitions with image urls

    key: "definitions"     value: a list of definitions
    key: "suggestions"     value: a list of suggestions if no matches are found
    """
    if "definitions" in d:
        if not stop_words:
            get_stop_words()
            
        defs = []
        d_append = defs.append
        for definition in d["definitions"]:
            def_list = definition.split()
            words = []
            w_append = words.append
            for word in def_list:
                word = word.strip()
            
                if (word not in stop_words and
                    len(word) > 2):
                    word = get_pict(word)
                w_append(word)
            d_append(words)
        d["definitions"] = defs
    return d



#Testing     
#print define("rose cut")
#print define("spontaneous combustion")
#print define("platypus")
#print define("gallows")
#print define("chain saw")
#print define("centrifugal force")

#print get_pict("potato")

#print define("pitato")
#print define("ninja")
#d = define("ninja")
#print d
#print pictify(d)

"""
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
print get_pict("potato")
"""

