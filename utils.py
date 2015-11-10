import urllib2, json


#takes the search query and appends to url
#run through api
#returns: the definition of the word (as a list or a string?)
#what to do if there is more than one definition 
def define(query):
    url = "https://api.pearson.com:443/v2/dictionaries/ldoce5/entries?search=%s"
    url = url % query
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)

    #how to get a single definition
    print r["results"][0]["senses"][0]["definition"][0]
    
#takes: one word from definition
#returns: image url 
def get_pict(word):
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



    
define("cat")
