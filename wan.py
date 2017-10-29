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

# 여러개의 키워드를 검색
# input : word seperated by space
# output : certain datastructure (tba)
# example
# input : 'fresh vegetable'
# output : JSON data above
def search_WAN(input_text):
    apikey = "9abec642-54e8-496a-9784-c98d0a428772"  # about key...
    url = "https://api.wordassociations.net/associations/v1.0/json/search?"
    # text_ = "welcome"
    # text_ = input_text.split(" ")
    lang_ = "en"
    params = {
        'apikey': apikey,
        'text': input_text,
        'lang': lang_
    }
    res = requests.get(url, params=params)
    data = res.json()['response']

    for elem in data:  # because it can response multiple keywords,
        keywords = elem['text']
        items = elem['items']
    return data

def get_pos(word):
    url = 'https://wordassociations.net/en/words-associated-with/' + word
    html = BeautifulSoup(requests.get(url).text, 'lxml')

    a = html.find('div', {'class' : 'n-container'})
    b = a.find('div', {'class' : 'n-content'})
    a = b.find('div', {'class' : 'n-content-right'})
    b = a.find('div', {'class' : 'dictionary'})
    a = b.find('div', {'class' : 'dictionary-content'})
    b = a.find('div', {'class' : 'dictionary-article'})
    a = b.contents[0].split(' ')[1][:-1]
    return a.lower()
