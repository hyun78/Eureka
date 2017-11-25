import glove
import numpy as np
from title_clear import *
import functools
from nltk.stem import WordNetLemmatizer as lt
CATEGORIES = [
			'human animal bird',
			'kind soft familiar',
			'machine robot technical architecture building',
			'fantasy adventure explore hunt hunter treasure'
			]
'''
'speed dash fast run race jump warp',
'ball roll bounce circle',
'song music classic rhythm sound piano',
'horror zombie blaxploitation'
]
'''
THREASHOLD = [
			0.4,
			0.4,
			0.4,
			0.4
			]
'''
0.4,
0.4,
0.4,
0.4
]
'''
#1. 없는 단어에 대해 -1 유형
#2. -1의 개수 -> length -> -1_2_-1 : 이렇게 dictionary


def generate_category_map(g,cat,th):
	lst = cat.split()
	lst=list(map( lambda x : global_map_generate(g,x,th), lst))
	return lst
def global_map_generate(glove_obj,word,th):
	try:
		widx1 = glove_obj.dictionary[word]
	except:
		print("no word exsit as {}".format(word))
		return []
	word_vec = glove_obj.word_vectors[widx1]
	dst = (np.dot(glove_obj.word_vectors, word_vec) / np.linalg.norm(glove_obj.word_vectors, axis=1) / np.linalg.norm(word_vec))
	word_ids = np.argsort(-dst) #[3 0 1 2]  input = [4,3,2,5]
	return [x for x in word_ids if dst[x] >th]

def read_glove_file(filename):
	g = glove.glove.Glove.load(filename)

	return g

def classify_word(g,input_word):
	type_class = [0 for i in range((len(CATEGORIES)))]
	input_word = lt().lemmatize(input_word.lower())
	try:
		input_word_idx = g.dictionary[input_word]

		for i in range(len(CATEGORY_MAP)):
			maps = CATEGORY_MAP[i]
			for map_ in maps:
				if  input_word_idx in map_:
					type_class[i] = 1

	except:
		type_class[-1] = -1
		print("no word available in dictionary: {}".format(input_word))

	return type_class
def similar_is(glove_obj,w1,w2):
	try:
		widx1 = glove_obj.dictionary[w1]
		widx2 = glove_obj.dictionary[w2]
		return similarity_query(glove_obj,glove_obj.word_vectors[widx1],widx2)
	except:
		return False



def similarity_query(glove_obj, word_vec, category_word_idx):
	dst = (np.dot(glove_obj.word_vectors, word_vec) / np.linalg.norm(glove_obj.word_vectors, axis=1) / np.linalg.norm(word_vec))
	if category_word_idx in glove_obj.inverse_dictionary:
		return dst[category_word_idx]
	else:
		return False
GLOVE_OBJ = read_glove_file('gf')
CATEGORY_MAP = list(map( lambda x: generate_category_map(GLOVE_OBJ,CATEGORIES[x],THREASHOLD[x]),range(len(CATEGORIES) )))

def test_routine(testword):
	type_vector = classify_word(GLOVE_OBJ,testword)
	print("type of {} is {}".format(testword,type_vector))
	title_list = clear_parser(select_section('database_crawling','arcade'),stereotype,stereotype_2)
	print(title_list)
	max_title_len = 10
	#types = [[] for i in range(max_title_len)]
	bigdic = {}
	for i in range(max_title_len):
		bigdic[str(i)] = [[] for i in range(max_title_len)]
	for title_dict in title_list:
		title = title_dict['title']
		title_len = len(title.split()) # 안동이 할 것이다.
		if title=='Adversal_input':
			continue
		temp_title = []
		nondict_cnt = 0
		for tw in title.split():
			try:
				twidx = GLOVE_OBJ.dictionary[tw.lower()]
			except:
				#print("no word exsit as {}".format(word))
				nondict_cnt = nondict_cnt +1
			temp_title.append(classify_word(GLOVE_OBJ,tw.lower()))

		#types[title_len].append([temp_title,title_len,title])
		#print(nondict_cnt, title_len, temp_title, title)
		bigdic[str(nondict_cnt)][title_len].append([temp_title,title_len,title])
	#types : [list of [list of type] , title]
	# ex : title = cookie run ->  types = [[[[0,1,1] ,[1,0,0]], cookie run] , [[[0,1,1] ,[1,0,0]], cookie run] , [[[0,1,1] ,[1,0,0]], cookie run]]
	# now : types =  [ [ [[0,1,1], [1,0,0]], 2, cookie run ], [ [[0,1,1], [1,0,0]], 2, cookie run ] , [ [[0,1,1], [1,0,0]], 2, cookie run ] ...]
	# type_statistics --> type_statistics[type_number] = number of type_number's instance ; [0,1,1] => 3.   [1,0,0] => 4
	# now : type number  = [ [[0,1,1],[1,0,0]],2 ] => 342  즉 마지막자리는 글자 수
	type_statistics = []
	for j in range(max_title_len):
		type_statistics.append([generate_type_statistics(bigdic[str(j)][i]) for i in range(max_title_len) if len(bigdic[str(j)][i])>0])

	return bigdic,type_statistics

def generate_type_statistics(type_list):
	types_statistics = {}
	for type_entity in type_list:
		word_type_list = type_entity[0]
		title_len = type_entity[1]
		title = type_entity[2]
		tn = type_num_calculate(word_type_list,title_len)
		try:
			types_statistics[tn][0]+=1
			types_statistics[tn][1].append(title)
		except:
			types_statistics[tn] = [1,[title]]

	return types_statistics

def type_num_calculate(word_type_list, title_len):
	wtlst = []
	temp = []
	for wt in word_type_list:
		if wt[-1] == -1:
			temp.append(-1)
		else:
			temp.append( int(''.join(str(i) for i in wt), 2) )
		temp.append('_')
	# now temp = list of typenum
	# ex : input=  [[1,1,1], [1,0,0]] => [7, 4]
	# type num is a string, 'typenums'+str(title_len)
	temp.append(title_len)
	type_num = ''.join(str(i) for i in temp)
	return type_num

if __name__=='__main__':
	bigdic, type_statistics = test_routine('')
	print (bigdic)
	print ('---------------------------------------------')
	print (type_statistics)
'''
for x in type_statistics[2].items():
	print(x[1][0], x[0])
print(type_statistics[1])
print(type_statistics[2])
print(type_statistics[3])
'''
