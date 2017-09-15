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
# res.json() produces all data like
# {'response': 
# 	[{'text': 'welcome', 
# 		'items': [	
# 					{'pos': 'adverb', 'item': 'Warmly', 'weight': 100}, 
# 					{'pos': 'adjective', 'item': 'Hearty', 'weight': 98}, 
# 					{'pos': 'adjective', 'item': 'Hospitable', 'weight': 94},  ... 
# 				]
# 		}
# 	], 
# 	'code': 200, 
# 	'request': {'text': ['welcome'], 'limit': 50, 'pos': 'noun,adjective,verb,adverb', 'type': 'stimulus', 'lang': 'en', 'indent': 'yes'}, 'version': '1.0'
# }

# start parsing

res.json()


