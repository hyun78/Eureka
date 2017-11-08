# Word Associations Network API 
# Making XML Query
from xml.etree.ElementTree import Element, dump
auth_key = "9abec642-54e8-496a-9784-c98d0a428772" #about key...
import urllib as urlb
import urlparse

url = "https://api.wordassociations.net/associations/v1.0/xml/search?"

apikey = auth_key
output = "xml"
q = "OpenAPI"
text_ = "Apple"
params = urlparse.urlencode({
	'apikey': apikey,
	'text': text_,
})

data = urlb.urlopen(url, params).read()



import requests

apikey = "9abec642-54e8-496a-9784-c98d0a428772" #about key...
url = "https://api.wordassociations.net/associations/v1.0/json/search?"
text_ = "welcome"
lang_ = "en"
params = {
			'apikey' : apikey,
			'text' : text_,
			'lang' : lang_
		}
res = requests.get(url, params=params)

	


