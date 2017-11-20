import glove
import numpy as np
from title_clear import *
import functools
CATEGORIES = [
			'human animal bird',
			'kind soft familiar',
			'machine robot technical architecture building',
			'fantasy adventure explore hunt hunter treasure',
			'speed dash fast run race jump warp',
			'ball roll bounce circle',
			'song music classic rhythm sound piano',
			'horror zombie blaxploitation'
			]
THREASHOLD = [
			0.4,
			0.4,
			0.4,
			0.4,
			0.4,
			0.4,
			0.4,
			0.4
			]



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
	try:
		
		input_word_idx = g.dictionary[input_word]
		
		for i in range(len(CATEGORY_MAP)):
			maps = CATEGORY_MAP[i]
			for map_ in maps:
				if  input_word_idx in map_:
					type_class[i] = 1

	except:
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
	
	types = []
	for title_dict in title_list:
		title = title_dict['title']
		#titlelen = title_dict['length'] 안동이 할 것이다.  
		if title=='Adversal_input':
			continue
		temp_title = []
		for tw in title.split():
			temp_title.append(classify_word(GLOVE_OBJ,tw.lower()))
		
		types.append([temp_title,title])
	#types : [list of [list of type] , title] 
	# ex : title = cookie run ->  types = [[[[0,1,1] ,[1,0,0]], cookie run] , [[[0,1,1] ,[1,0,0]], cookie run] , [[[0,1,1] ,[1,0,0]], cookie run]]
	# type_statistics --> type_statistics[type_number] = number of type_number's instance
	# 
	types_num =list(map(lambda t :  list( map( lambda z : ( functools.reduce(lambda x,y : x*2+y, z)), t[0] )),types))
	type_statistics = [0 for i in range(pow(2,len((CATEGORIES))))]
	for t in types_num:
		for tn in t:
				type_statistics[tn]+=1
	return types,type_statistics
def type_test(type_map,type_index):
	res = []
	for type_entry in type_map:
		for te in type_entry[0]:
			if functools.reduce(lambda x,y : x*2+y, te)==type_index:
				res.append(type_entry[1])
				break
	return res
