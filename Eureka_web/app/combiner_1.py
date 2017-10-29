from random import randint
from wan import *
import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import re
import requests
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


#1 Abbreviation #
def generate_abbreviation(associated_words_set,n):
	name_list = phrase_generation(associated_words_set,n)
	
	name_string = '+'.join(name_list)
	url = 'https://acronymify.com/search?q='+name_string
	request = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
	data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
	bs = BeautifulSoup(data,'lxml')
	ent = bs.find_all('tr')
	m = len(ent)
	res = []
	for i in range(1,m):
		res.append(ent[i].find_all('a')[0].text)
	return res

#2 Acronym
def generate_acronym(associated_words_set,n):
	name_list = phrase_generation(associated_words_set,n)
	ABB = ""
	for word in name_list:
		ABB+=word[0].upper()
	return ABB,name_list
# helper function

# Helper 1
def phrase_generation(associated_words_set,n):
	a = randint(2,n) # 단어 수 결정 
	n_list = [i for i in range(0,n)]
	name_list = []
	# acronym을 만들 단어를 랜덤하게 생성 
	for i in range(a):
		k = n_list.pop(randint(0,len(n_list)-1))
		print('k : ',k)
		name_list.append(get_random_associate_word_of_kth_keyword(associated_words_set,k))
	return name_list
# Helper 2
def get_random_associate_word_of_kth_keyword(associated_words_set,k):
	
	i =  randint(0,49)
	print (' get ith number :',i)
	word = associated_words_set[k]['items'][i]['item']
	return word

# for test
def test():
	text_string = 'fresh water white cool'
	n = len(text_string.split(' '))
	associated_words_set = search_WAN('fresh water white cool')
	abb = generate_acronym(associated_words_set,n)
	print(abb)
	return