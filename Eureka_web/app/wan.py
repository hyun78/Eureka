# Word Associations Network API 
# Making XML Query

import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import re
import requests


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


	
#여러개의 키워드를 검색 
# input : word seperated by space
# output : certain datastructure (tba)
# example
# input : ['fresh', 'vegetable']
# output : JSON data above
def search_WAN(input_text):
	apikey = "9abec642-54e8-496a-9784-c98d0a428772" #about key...
	url = "https://api.wordassociations.net/associations/v1.0/json/search?"
	#text_ = "welcome"
	#text_ = input_text.split(" ")
	lang_ = "en"
	params = {
				'apikey' : apikey,
				'text' : input_text,
				'lang' : lang_
			}
	res = requests.get(url, params=params)
	data = res.json()['response']

	for elem in data: # because it can response multiple keywords, 
		keywords = elem['text']
		items = elem['items']
	return data

# input parsing : Hangul word -> English words
def word_translate(token):
	translated_list = []
		

	return translated_list

# word list- > pronunciation list in korean
def get_korean_pronunciation(word_list):
	result = []
	for word in word_list:
		request = urllib.request.Request("http://aha-dic.com/View.asp?word="+parse.quote(word))
		data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
		bs = BeautifulSoup(data,'lxml')
		ent = bs.find_all('span',attrs={'class':'phoneticKor'})
		if len(ent):
			result.append(ent[0].text[1:-1])
	return result

#다음 검색사전에서 크롤링
def translate(keyword):
	#다음 검색사전 활용 
	request = urllib.request.Request("http://dic.daum.net/search.do?q="+parse.quote(keyword)+"&dic=eng") 
	data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
	bs = BeautifulSoup(data,'lxml')
	#파싱 
	ent = bs.find_all('div',attrs={'class':'search_box #box'}) 
	if len(ent): # 동음이의어 존재 
		ent = ent[0].find_all('span',attrs={'class':'txt_search'})
		
		words = []
		# for elem in ent:
		# 	res = elem.find_all('span',attrs={'class':'txt_search'}) 
		
		for word in ent:
			words.append(word.text.strip())
			print(word.text)
		return stopword_removal((words))
	else: # 동음이의어 없응
		text = bs.text
		pattern = 'kew\d+'
		model = re.compile(pattern)
		key_id = model.findall(text)[0]
		print('key_id',key_id) 
		words = find_by_key_dic(key_id)
	return stopword_removal((words))


def find_by_key_dic(key_id):
	#찾은 key로 다시 사전 검색하기 
	request = urllib.request.Request("http://dic.daum.net/word/view.do?wordid="+key_id)
	data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
	bs = BeautifulSoup(data,'lxml')
	res = bs.find_all('span',attrs={'class':'txt_mean'})
	words = []
	for word in res:
		words.append(word.text.strip())
		print(word.text)
	return words

#관사 제거 , 두 단어 이상 제거	
def stopword_removal(word_list):
  stopword = ['an','a','the']
  result = []
  for item in word_list:
    temp = item.split(' ')    
    tmp = []
    for elem in temp:
      if elem not in stopword:
        tmp.append(elem)
    if len(tmp) <2:
	    result.append(' '.join(tmp))
  return result



