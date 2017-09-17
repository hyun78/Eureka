# Word Associations Network API 
# Making XML Query

import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import re
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

data = res.json()['response']

for elem in data: # because it can response multiple keywords, 
	keywords = elem['text']
	items = elem['items']
	
# input parsing : Hangul word -> English words

def word_translate(token):
	translated_list = []
		

	return translated_list

#다음 검색사전에서 크롤링
def translate(keyword):
  #다음 검색사전 활용 
  request = urllib.request.Request("http://dic.daum.net/search.do?q="+parse.quote(keyword)+"&dic=eng") 
  data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
  bs = BeautifulSoup(data,'lxml')
  #파싱 
  ent = bs.find_all('div',attrs={'class':'cleanword_type kuke_type'}) 
  res = ent[0].find_all('span',attrs={'class':'txt_search'}) 
  words = []
  for word in res:
    words.append(word.text)
    print(word.text)
  return words





