


FILE_NAME = 'data_arcade.json' # pre-defined file name
from collections import OrderedDict
import json
import random
def read_json_file(filename):
   data = None
   with open(filename, encoding="utf-8") as data_file:
      data = json.load(data_file, object_pairs_hook=OrderedDict)
   return data
#keyword가 가지는 가장 많은 title suffix/infix/prefix 단어 추출
def read_database(filename):
	data = read_json_file(filename)
	return data

def max_key_extraction_keyword(dictionary,keyword):
	try:
		keys = list(dictionary[keyword].keys())
		res = []
		sum_max = 0
		sum_temp = 0
		max_key = None
		for key in keys:
			lst = dictionary[keyword][key].keys()
			for item in lst:
				scope = item.split('_')[-1]
				if scope=='local':
					sum_temp +=dictionary[keyword][key][item]
			if sum_temp>sum_max:
				sum_max = sum_temp
				max_key = key
			sum_temp = 0
		return max_key
	except:
		print("no key exist in database : ",keyword)
		return None

#templete :
#return 0 1 2 for each prefix, infix, and suffix 
def type_casting(templete):
	try:
		tag = templete.split('_')[0]
		if (tag == 'pre'):
			return 'pre'
		if (tag == 'mid'):
			return 'mid'
		if (tag =='suf'):
			return 'suf'
		return -1
	except:
		return -1
def extract_item(templete):
	try:
		item = templete.split('_')[-1]
		return item
	except:
		return ''
	return ''
#words sets 은 list로 주어진다
def combine_name_with_templete(templete,word_sets,word_length):
	tag_ = type_casting(templete)
	item = extract_item(templete)
	n = 10
	combined_words = []
	
	if (tag_ =='pre'):
		for i in range(n):
			wlst = pick_n_word_from_word_list(word_sets,word_length)
			combined_word = generate_prefix_word(item,wlst)
			combined_words.append(combined_word)
	elif(tag_ =='mid'):
		for i in range(n):	
			wlst = pick_n_word_from_word_list(word_sets,word_length)
			random_index = random.randint(0,word_length-1)
			combined_word = generate_inffix_word(item,wlst,random_index)
	elif(tag_ =='suf'):
		for i in range(n):	
			wlst = pick_n_word_from_word_list(word_sets,word_length)
			combined_word = generate_suffix_word(item,wlst)
			combined_words.append(combined_word)
	else:
		return []

	return combined_words
def generate_prefix_word(item,wlst):
	res = item
	for w in wlst:
		res += (' ' + w)
	return res
def generate_suffix_word(item,wlst):
	res = ''
	for w in wlst:
		res +=  (w + ' ')
	res += item
	return res
def generate_inffix_word(item,wlst,idx):
	res = ''
	i = 0
	for w in wlst:
		if idx!=i:
			res +=  (w + ' ')
		else:
			res+= (item+ ' ')
			res += (w + ' ')
	return res
def pick_n_word_from_word_list(word)
def main_routine():
	data = read_database(FILE_NAME)
	example_keywords = ['chocolate','candy','shoot']
	related_word_list = ['Cookie','cream','crunch','cracker','sweet','crush','sniper','blaster','kill']
	print("example keywords: ",example_keywords)
	for key in example_keywords:
		templete = max_key_extraction_keyword(data,key)
		print("keyword : ",key,"\nmost used : ",templete)
		print("generated names:",combine_name_with_templete(templete,related_word_list))

	
	
