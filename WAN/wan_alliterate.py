# -*- coding : utf-8 -*-
# Word Associations Network API
# Making XML Query

import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import re
import requests
from wan import *
from Vocabulary_104.vocabulary.vocabulary import Vocabulary as vb
from time import time as t

# Helper functions
# get pronunciation from input_word
def pronunciation(input_word):
    url_test = "http://texttophonetic.appspot.com/ipa?c="
    request = urllib.request.Request(url_test+input_word)
    data = str(urllib.request.urlopen(request).read().decode()) #UTF-8 encode
    data = data[0:-1] # erase last space
    if (data[0]=='[' and data[-1]==']'):
        data = data[1:-1]
    data = data.replace('\'','') #erase accent 1
    data = data.replace(',','') #erase accent 2
    if (data.find(' ')!=-1):
        data = data[:data.find(' ')]
    data_len = len(data)
    datascan = 0
    output_pronunciation = []
    while(datascan<data_len):
        if data[datascan]!='\\':
            output_pronunciation.append(data[datascan])
            datascan = datascan+1
        else:
            output_pronunciation.append(pronunciation_dict[data[datascan+2:datascan+6].upper()])
            datascan = datascan+6
    return output_pronunciation

# get uppercase if word is alphabet
def helper_upper(word):
    if word in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()):
        return word.upper()
    return word

#dictionary of pronunciation in English
pronunciation_dict ={
'0251' :'ɑ','0253' :'ɓ', '0254' :'ɔ',
#'0255' :'ɕ', '0256' :'ɖ', '0257' :'ɗ',
'0258' :'ɘ', '0259' :'ə',
#'025A' :'ɚ',
'025B' :'ɛ', '025C' :'ɜ',
#'025D' :'ɝ', '025E' :'ɞ', '025F' :'ɟ', '0260' :'ɠ', '0261' :'ɡ', '0262' :'ɢ', '0263' :'ɣ', '0264' :'ɤ','0265' :'ɥ', '0266' :'ɦ', '0267' :'ɧ', '0268' :'ɨ', '0269' :'ɩ',
#'026A' :'ɪ', '026B' :'ɫ', '026C' :'ɬ', '026D' :'ɭ', '026E' :'ɮ', '026F' :'ɯ',
#'0270' :'ɰ', '0271' :'ɱ', '0272' :'ɲ',
'0273' :'ɳ', #'0274' :'ɴ',
#'0275' :'ɵ', '0276' :'ɶ', '0277' :'ɷ', '0278' :'ɸ', '0279' :'ɹ',
#'027A' :'ɺ', '027B' :'ɻ', '027C' :'ɼ', '027D' :'ɽ', '027E' :'ɾ', '027F' :'ɿ',
#'0280' :'ʀ', '0281' :'ʁ', '0282' :'ʂ',
'0283' :'ʃ',
#'0284' :'ʄ', '0285' :'ʅ', '0286' :'ʆ', '0287' :'ʇ', '0288' :'ʈ', '0289' :'ʉ', '028A' :'ʊ', '028B' :'ʋ',
'028C' :'ʌ',
#'028D' :'ʍ', '028E' :'ʎ', '028F' :'ʏ', '0290' :'ʐ', '0291' :'ʑ', '0292' :'ʒ', '0293' :'ʓ', '0294' :'ʔ','0295' :'ʕ', '0296' :'ʖ', '0297' :'ʗ', '0298' :'ʘ', '0299' :'ʙ',
#'029A' :'ʚ', '029B' :'ʛ', '029C' :'ʜ', '029D' :'ʝ', '029E' :'ʞ', '029F' :'ʟ',
#'02A0' :'ʠ', '02A1' :'ʡ', '02A2' :'ʢ',
'02A3' :'ʣ', '02A4' :'ʤ',
#'02A5' :'ʥ', '02A6' :'ʦ', '02A7' :'ʧ', '02A8' :'ʨ', '02A9' :'ʩ',
#'02AA' :'ʪ', '02AB' :'ʫ', '02AC' :'ʬ', '02AD' :'ʭ', '02AE' :'ʮ', '02AF' :'ʯ',
'00E6' : 'æ', '03B8' : 'θ'
}

def alliterate(kws):
    num = len(kws)
    # some useful constant lists
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    pron_alpha = list(pronunciation_dict.values())
    alphabet = alphabet + pron_alpha + [":"]
    # elapsed time checker - start time
    start_time = t()

    apikey = "9abec642-54e8-496a-9784-c98d0a428772"  # about key...
    url = "https://api.wordassociations.net/associations/v1.0/json/search?"
    lang_ = "en"
    waset = []

    #print (search_WAN(kws))

    data = search_WAN(kws)
    for i in range(len(data)):
        subdict = {'text':data[i]['text'],'noun':{}, 'adjective':{},'verb':{}, 'adverb':{}}
        for letters in alphabet:
            subdict['noun'][letters] = []
            subdict['adjective'][letters] = []
            subdict['verb'][letters] = []
            subdict['adverb'][letters] = []
            subdict['noun']['suf'+letters] = []
            subdict['adjective']['suf'+letters] = []
            subdict['verb']['suf'+letters] = []
            subdict['adverb']['suf'+letters] = []
        for elements in data[i]['items']:
            #print (elements['item'], pronunciation(elements['item'].lower()))
            elements['pronunciation']=pronunciation(elements['item'].lower())
            subdict[elements['pos']][helper_upper(elements['pronunciation'][0])].append(elements)
            subdict[elements['pos']]['suf'+helper_upper(elements['pronunciation'][-1])].append(elements)
        waset.append(subdict)

    #for i in range(num):
    #    params = {
    #        'apikey': apikey,
        #'text': text_,
    #        'text' : kws[i],
    #        'lang': lang_
    #    }
    #    res = requests.get(url, params=params)
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
    """
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
    """
    #print(waset)
    #print(waset[0]['text'], waset[1]['text'], waset[2]['text'])

    alliteration = {}
    similarity_level = 'NLMH'

    for x in range(num):
        for y in range(x,num):
            if x==y:
                continue
            else:
                alliteration[kws[x]+','+kws[y]]={'front':{'ADJ+N':{'N':[],'L':[],'M':[],'H':[]},'N+N':{'N':[],'L':[],'M':[],'H':[]},'N+ADJ':{'N':[],'L':[],'M':[],'H':[]}}, 'back':{'ADJ+N':{'N':[],'L':[],'M':[],'H':[]},'N+N':{'N':[],'L':[],'M':[],'H':[]},'N+ADJ':{'N':[],'L':[],'M':[],'H':[]}}}
    #print(alliteration)

    # Merging
    for x in range(num):
        for y in range(x,num):
            if x==y:
                continue
            else:
                for letters in alphabet:
                    first = ""
                    second = ""
                    letters=helper_upper(letters)
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
                            first_p = first_item['pronunciation']
                            for second_item in waset[y]['noun'][letters]:
                                second = second_item['item']
                                second_p = second_item['pronunciation']
                                cnt = 0
                                for i in range(min(len(first_p), len(second_p), 3)):
                                    if first_p[i] == second_p[i]:
                                        cnt = cnt + 1
                                    else: break

                                alliteration[kws[x] + ',' + kws[y]]['front']['ADJ+N'][similarity_level[cnt]].append(first + " " + second + " " + str(first_p[:cnt]))

                    # noun+noun
                    if (first_noun_num * second_noun_num != 0):
                        for first_item in waset[x]['noun'][letters]:
                            first = first_item['item']
                            first_p = first_item['pronunciation']
                            for second_item in waset[y]['noun'][letters]:
                                second = second_item['item']
                                second_p = second_item['pronunciation']
                                cnt = 0
                                for i in range(min(len(first_p), len(second_p), 3)):
                                    if first_p[i] == second_p[i]:
                                        cnt = cnt + 1
                                    else: break
                                alliteration[kws[x] + ',' + kws[y]]['front']['N+N'][similarity_level[cnt]].append(first + " " + second + " " + str(first_p[:cnt]))

                    # noun+adj
                    if (first_noun_num * second_adj_num != 0):
                        for first_item in waset[x]['noun'][letters]:
                            first = first_item['item']
                            first_p = first_item['pronunciation']
                            for second_item in waset[y]['adjective'][letters]:
                                second = second_item['item']
                                second_p = second_item['pronunciation']
                                cnt = 0
                                for i in range(min(len(first_p), len(second_p), 3)):
                                    if first_p[i] == second_p[i]:
                                        cnt = cnt + 1
                                    else: break
                                alliteration[kws[x] + ',' + kws[y]]['front']['N+ADJ'][similarity_level[cnt]].append(first + " " + second + " " + str(first_p[:cnt]))

                    # back
                    # adj+noun ,noun+noun, noun+adj
                    # adj+noun
                    if (suf_first_adj_num * suf_second_noun_num != 0):
                        for first_item in waset[x]['adjective']['suf'+letters]:
                            first = first_item['item']
                            first_p = first_item['pronunciation']
                            for second_item in waset[y]['noun']['suf'+letters]:
                                second = second_item['item']
                                second_p = second_item['pronunciation']
                                cnt = 0
                                for i in range(min(len(first_p), len(second_p), 3)):
                                    if first_p[-1-i] == second_p[-1-i]:
                                        cnt = cnt + 1
                                    else: break
                                if not (cnt==1 and first_p[-1]==":"):
                                    alliteration[kws[x]+','+kws[y]]['back']['ADJ+N'][similarity_level[cnt]].append(first + " " + second+" "+str(first_p[-cnt:]))
                    # noun+noun
                    if (suf_first_noun_num * suf_second_noun_num != 0):
                        for first_item in waset[x]['noun']['suf'+letters]:
                            first = first_item['item']
                            first_p = first_item['pronunciation']
                            for second_item in waset[y]['noun']['suf'+letters]:
                                second = second_item['item']
                                second_p = second_item['pronunciation']
                                cnt = 0
                                for i in range(min(len(first_p), len(second_p), 3)):
                                    if first_p[-1-i] == second_p[-1-i]:
                                        cnt = cnt + 1
                                    else: break
                                if not (cnt==1 and first_p[-1]==":"):
                                    alliteration[kws[x]+','+kws[y]]['back']['N+N'][similarity_level[cnt]].append(first + " " + second+" "+str(first_p[-cnt:]))
                    #noun + adj
                    if (suf_first_noun_num * suf_second_adj_num != 0):
                        for first_item in waset[x]['noun']['suf'+letters]:
                            first = first_item['item']
                            first_p = first_item['pronunciation']
                            for second_item in waset[y]['adjective']['suf'+letters]:
                                second = second_item['item']
                                second_p = second_item['pronunciation']
                                cnt = 0
                                for i in range(min(len(first_p), len(second_p), 3)):
                                    if first_p[-1-i] == second_p[-1-i]:
                                        cnt = cnt + 1
                                    else: break
                                if not (cnt==1 and first_p[-1]==":"):
                                    alliteration[kws[x]+','+kws[y]]['back']['N+ADJ'][similarity_level[cnt]].append(first + " " + second+" "+str(first_p[-cnt:]))
    # elapsed time checker - end time
    end_time = t()
    print(end_time - start_time)
    return alliteration

#test
keywords = ["halal","vegetable","lunch"] #input for test
print(alliterate(keywords))

#for elem in data:  # because it can response multiple keywords,
#    keywords = elem['text']
#    items = elem['items']
