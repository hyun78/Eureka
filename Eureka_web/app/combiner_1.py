from random import randint
from wan import *
import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import re
import requests
from syllabipy.sonoripy import SonoriPy
#input : specified data structure as below
# {
# keyword_1 : key1
# 	associated_1 : word1
# 	associated_2 : word2
# 	...
# keyword_2 : 
# 	associated_1 : word1
# 	associated_2 : word2
# 	...
# ...
# keyword_n : key1
#   ...
# }


#1 Abbreviation 
# n = 키워드 수 
# m = 줄일 단어의 수 ex: Federal express 의 경우 m=2
def generate_abbreviation_crawling(associated_words_set,n,m):
	name_list = []
	for i in range(n*m):
		name_list.append(random_phrase_generation(associated_words_set,n,m))
	result = {}
	for p in name_list:
		name_string = '+'.join(p)
		url = 'https://acronymify.com/search?q='+name_string
		request = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
		data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
		bs = BeautifulSoup(data,'lxml')
		ent = bs.find_all('tr')
		m = len(ent)
		res = []
		
		for i in range(1,m):
			tup = [ent[i].find_all('a')[0].text,ent[i].find_all('td')[1].text]
			res.append(tup)
		result[' '.join(p)] = res

	return result

def generate_abbreviation_handmade(associated_words_set,n,m):
	name_list = []
	for i in range(n*m):
		name_list.append(random_phrase_generation(associated_words_set,n,m))
	result = {}
	for p in name_list:
		res = []
		full_word = ""
		abb = ""
		
		last = len(p)-1
		idx = 0
		for w in p:
			tokens = SonoriPy(w.lower())
			temp_n= len(tokens)
			if idx==0:
				start = 0	
			elif idx==last:
				start = temp_n-1
			else:
				if temp_n!=1:
					start = randint(0,temp_n-2)
				else:
					start = 0
			idx +=1
			abb += tokens[start]
			tokens[start] = tokens[start].upper()
			for t in tokens:
				full_word += t
			full_word += " "		
		result[' '.join(p)] = abb.upper(),full_word
	return result

#2 Acronym
def generate_acronym(associated_words_set,n,m):
	name_list = phrase_generation(associated_words_set,n,m)
	ABB_list = []
	for p in name_list:
		ABB = ""
		for word in p:
			ABB+=word[0].upper()
		ABB_list.append([ABB,p])
	return ABB_list
# helper function

# Helper 1
def random_phrase_generation(associated_words_set,n,m):
	
	n_list = [i for i in range(0,n)]
	name_list = []
	# acronym을 만들 단어를 랜덤하게 생성 
	for i in range(m):
		k = n_list.pop(randint(0,len(n_list)-1))
		name_list.append(get_random_associate_word_of_kth_keyword(associated_words_set,k))
	return name_list
# Helper 2
def get_random_associate_word_of_kth_keyword(associated_words_set,k):
	
	i =  randint(0,50)
	print (' get ith number :',i)
	if (i==50):
		word = associated_words_set[k]['text']
	else:
		word = associated_words_set[k]['items'][i]['item']
	return word
# Helper 3
# 단어를 모음과 자음으로 쪼갠다. 
# ex : crunch -> cr u nch 
# ex : king -> king 

def tokenize(word):
	return None
# for test
def test():
	text_string = 'fresh water white cool'
	n = len(text_string.split(' '))
	text_list = text_string.split(' ')
	associated_words_set = search_WAN(text_list)
	acrnym= generate_acronym(associated_words_set,n)
	abb = generate_abbreviation(associated_words_set,n)
	print(abb)
	print(acrnym)
	return