# Word Associations Network API 
# Making XML Query

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

	


