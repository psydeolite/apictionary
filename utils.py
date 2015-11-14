from threading import Thread
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
    Runs an api search on a string query and returns the definition(s) of the word as a dictionary

    calls: get_def, remove_stupid_tags, get_suggestions

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

    
    
def get_pic(word, def_list, i):
    """
    Runs a word through a picture search and returns an image url as a string
    """
    pic = word.strip()
    if (pic not in stop_words and
          len(pic) > 2):

        url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&format=json&nojsoncallback=1&media=photos&text=%s&sort=relevance&extras=url_q"
        key = "e0e0c259e7e2a1f07f6c8e6a74579f12"
        
        url = url % (key, pic)
        request = urllib2.urlopen(url)
        result = request.read()
        r = json.loads(result)

        try:
            pic = r["photos"]["photo"][0]["url_q"]
        except:
            pass
        
    def_list[i] = pic

    

def get_pics(def_list):
    """
    Replaces words in list def_list with image urls
    calls: get_pic
    """
    threads = [None] * len(def_list)
    
    for i in range(len(def_list)):
        threads[i] = Thread(target = get_pic,
                            args = (def_list[i], def_list, i))

    [t.start() for t in threads]    
    [t.join() for t in threads]
    
    return def_list

    
def pictify(word):
    """  
    Defines string words and replaces the words in the dictionary with image urls
    calls: define, get_pics
    returns: a dictionary of definitions with image urls

    key: "definitions"     value: a list of definitions
    key: "suggestions"     value: a list of suggestions if no matches are found
    """
    if not stop_words:
        get_stop_words()

    d = define(word)
    
    if "definitions" in d:
        defs = []
        
        for definition in d["definitions"]:
            def_list = definition.split()
            defs.append(get_pics(def_list))

        d["definitions"] = defs
            
    return d



#Testing     
#print define("rose cut")
#print define("spontaneous combustion")
#print define("platypus")
#print define("gallows")
#print define("chain saw")
#print define("centrifugal force")

#print get_pic("potato")
#print get_pic("ninja")
#print define("pitato")
#print define("ninja")

print pictify("spontaneous combustion")

