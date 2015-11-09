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
#returns image url 
def picture(word):

    
#takes: the search query
#replaces certain words with image urls
#returns: something
def pictify(query):
    d = define(query)



    
define("cat")
