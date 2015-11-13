import urllib2
import json
import xmltodict
import random

stop_words = []

def get_stop_words():
    global stop_words
    file = open("static/stop.csv", 'r')
    for line in file:
        stop_words.append(line.strip())
    file.close()
    

def define(query):
    """
    Runs an api search on a word and returns the definition(s) of the word

    params: query, a string

    returns: a list of definitions
    """    
    q = query.replace(" ", "+")
    key = "f3815ee8-aa94-4c97-a283-fbf3cb5d2c05"
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=%s"
    url = url % (q, key)
    request = urllib2.urlopen(url)
    result = request.read()

    result = remove_stupid_tags(result)
    r = xmltodict.parse(result)
    out = json.loads(json.dumps(r))

    #print result
    #print "\n"
    #print out

    defs = []
    entries = out["entry_list"]["entry"]
    
    if isinstance(entries, list):
        for res in entries:
            defs += get_def(res, query)
    elif isinstance(entries, dict):
        defs = get_def(entries, query)
    return defs
    

def remove_stupid_tags(text):
    """
    Primes the xml by removing unecessary tags (ex. styling)
    
    params: the text to be primed - string

    returns: a cleaner version of the xml - string
    """
    new = text.replace("<it>", "")
    new = new.replace("</it>", "")
    new = new.replace("<d_link>", "")
    new = new.replace("</d_link>", "")
    new = new.replace("<sx>", "")
    new = new.replace("</sx>", "")
    new = new.replace("<cat>", "")
    new = new.replace("</cat>", "")
    new = new.replace("<ca>", ", ")
    new = new.replace("</ca>", "")
    
    return new
    
    
def get_def(res, query):
    """
    Finds and returns the definition for a specific entry in the dictionary
    
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

        for entry in d:
            if (isinstance(d, list) and
                    isinstance(entry, unicode):
                defs.append(str(entry)[1:])

            elif (isinstance(d, dict)):
                if (isinstance(d[entry], unicode) and
                    is_legit_def(d[entry], query)):
                    defs.append(str(d[entry])[1:])

            elif isinstance(d[entry], dict):
                try:
                    if is_legit_def(d[entry["#text"]], query):
                        defs.append(str(d[entry["#text"]])[1:])
                except:
                    pass
          
    return defs


def is_legit_def(definition, word):
    """
    Some tests for whether a string is a def because stupid api
    params: definition - string
            the search word - string

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
    Run a word through a picture search and return an image url

    params: the search word - string

    returns: a url for a picture - string
    """
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&format=json&nojsoncallback=1&media=photos&text=%s&sort=relevance&extras=url_q"
    key = "e0e0c259e7e2a1f07f6c8e6a74579f12"
    url = url % (key, word)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)

    bound =  len(r["photos"]["total"])

    index = random.randrange(0, bound)
    pic = word
    try:
        pic = r["photos"]["photo"][index]["url_q"]
    except:
        pass
    return pic 
    

    

def pictify(query):
    """  
    Replaces the words in the definition with image urls

    params: query, a string

    returns: a list of definitions with image urls
    """
    if not stop_words:
        get_stop_words()
        
    d = define(query)
    defs = []
    for definition in d:
        def_list = definition.split()
        words = []
        for word in def_list:
            word = word.strip()
            
            if (word not in stop_words and
                    len(word) > 2):
                word = get_pict(word)
                
            words.append(word)
        defs.append(words)
    return defs



#Testing     
#print define("rose cut")
#print define("spontaneous combustion")
#print define("platypus")
#print define("gallows")
#print define("chain saw")
#print define("centrifugal force")

#print get_pict("violent")
#print pictify("garrulous")

print define("garrulous")

