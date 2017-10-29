# -*- coding : utf-8 -*-
# Word Associations Network API
# Making XML Query

import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import re
import requests
from wan import *

alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
kws = ["halal","vegetable","lunch"] #<-input 가능하게끔
num = len(kws)

apikey = "9abec642-54e8-496a-9784-c98d0a428772"  # about key...
url = "https://api.wordassociations.net/associations/v1.0/json/search?"
#text_ = "welcome"
lang_ = "en"
waset = []

for i in range(num):
    params = {
        'apikey': apikey,
        #'text': text_,
        'text' : kws[i],
        'lang': lang_
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
    subdict = {'text':data[0]['text'],'noun':{}, 'adjective':{},'verb':{}, 'adverb':{}}
    for letters in alphabet:
        subdict['noun'][letters] = []
        subdict['adjective'][letters] = []
        subdict['verb'][letters] = []
        subdict['adverb'][letters] = []
        subdict['noun']['suf'+letters] = []
        subdict['adjective']['suf'+letters] = []
        subdict['verb']['suf'+letters] = []
        subdict['adverb']['suf'+letters] = []
    for elements in data[0]['items']:
        subdict[elements['pos']][elements['item'][0]].append(elements)
        subdict[elements['pos']]['suf'+elements['item'][-1].upper()].append(elements)
    waset.append(subdict)

print(waset)
print(waset[0]['text'], waset[1]['text'], waset[2]['text'])

alliteration = {}
similarity_level = 'NLMH'

for x in range(num):
    for y in range(x,num):
        if x==y:
            continue
        else:
            alliteration[kws[x]+','+kws[y]]={'front':{'ADJ+N':{'L':[],'M':[],'H':[]},'N+N':{'L':[],'M':[],'H':[]},'N+ADJ':{'L':[],'M':[],'H':[]}}, 'back':{'ADJ+N':{'L':[],'M':[],'H':[]},'N+N':{'L':[],'M':[],'H':[]},'N+ADJ':{'L':[],'M':[],'H':[]}}}
print(alliteration)

#fronts
for x in range(num):
    for y in range(x,num):
        if x==y:
            continue
        else:
            for letters in alphabet:
                first = ""
                second = ""
                first_adj_num = len(waset[x]['adjective'][letters])
                first_noun_num = len(waset[x]['noun'][letters])
                second_adj_num = len(waset[y]['adjective'][letters])
                second_noun_num = len(waset[y]['noun'][letters])

                suf_first_adj_num = len(waset[x]['adjective']['suf'+letters])
                suf_first_noun_num = len(waset[x]['noun']['suf'+letters])
                suf_second_adj_num = len(waset[y]['adjective']['suf'+letters])
                suf_second_noun_num = len(waset[y]['noun']['suf'+letters])
                # front
                # adj+noun ,noun+noun, noun+adj
                # adj+noun
                if (first_adj_num * second_noun_num != 0):
                    for first_item in waset[x]['adjective'][letters]:
                        first = first_item['item']
                        for second_item in waset[y]['noun'][letters]:
                            second = second_item['item']
                            cnt = 0
                            for i in range(min(len(first), len(second), 3)):
                                if first[i] == second[i]:
                                    cnt = cnt + 1
                            alliteration[kws[x]+','+kws[y]]['front']['ADJ+N'][similarity_level[cnt]].append(first + " " + second)
                # noun+noun
                if (first_noun_num * second_noun_num != 0):
                    for first_item in waset[x]['noun'][letters]:
                        first = first_item['item']
                        for second_item in waset[y]['noun'][letters]:
                            second = second_item['item']
                            cnt = 0
                            for i in range(min(len(first), len(second), 3)):
                                if first[i] == second[i]:
                                    cnt = cnt + 1
                            alliteration[kws[x]+','+kws[y]]['front']['N+N'][similarity_level[cnt]].append(first + " " + second)
                # noun+adj
                if (first_noun_num * second_adj_num != 0):
                    for first_item in waset[x]['noun'][letters]:
                        first = first_item['item']
                        for second_item in waset[y]['adjective'][letters]:
                            second = second_item['item']
                            cnt = 0
                            for i in range(min(len(first), len(second), 3)):
                                if first[i] == second[i]:
                                    cnt = cnt + 1
                            alliteration[kws[x]+','+kws[y]]['front']['N+ADJ'][similarity_level[cnt]].append(first + " " + second)

                # back
                # adj+noun ,noun+noun, noun+adj
                # adj+noun
                if (suf_first_adj_num * suf_second_noun_num != 0):
                    for first_item in waset[x]['adjective']['suf'+letters]:
                        first = first_item['item']
                        for second_item in waset[y]['noun']['suf'+letters]:
                            second = second_item['item']
                            cnt = 0
                            for i in range(min(len(first), len(second), 3)):
                                if first[-1-i] == second[-1-i]:
                                    cnt = cnt + 1
                            alliteration[kws[x]+','+kws[y]]['back']['ADJ+N'][similarity_level[cnt]].append(first + " " + second)

                if (suf_first_noun_num * suf_second_noun_num != 0):
                    for first_item in waset[x]['noun']['suf'+letters]:
                        first = first_item['item']
                        for second_item in waset[y]['noun']['suf'+letters]:
                            second = second_item['item']
                            cnt = 0
                            for i in range(min(len(first), len(second), 3)):
                                if first[-1-i] == second[-1-i]:
                                    cnt = cnt + 1
                            alliteration[kws[x]+','+kws[y]]['back']['N+N'][similarity_level[cnt]].append(first + " " + second)

                if (suf_first_noun_num * suf_second_adj_num != 0):
                    for first_item in waset[x]['noun']['suf'+letters]:
                        first = first_item['item']
                        for second_item in waset[y]['adjective']['suf'+letters]:
                            second = second_item['item']
                            cnt = 0
                            for i in range(min(len(first), len(second), 3)):
                                if first[-1-i] == second[-1-i]:
                                    cnt = cnt + 1
                            alliteration[kws[x]+','+kws[y]]['back']['N+ADJ'][similarity_level[cnt]].append(first + " " + second)


print (alliteration)

#for elem in data:  # because it can response multiple keywords,
#    keywords = elem['text']
#    items = elem['items']
