import glove
import numpy as np
from title_clear import *

CATEGORIES = [
			'human animal bird',
			'kind soft familiar',
			'machine robot technical architecture building',
			'adventure explore hunt hunter treasure',
			'speed dash fast run race jump warp']
THREASHOLD = [
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
		print(input_word)
		input_word_idx = g.dictionary[input_word]
		print(input_word_idx,input_word)
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
	for title_dict in title_list[:100]:
		title = title_dict['title']
		if title=='Adversal_input':
			continue
		temp_title = []
		for tw in title.split():
			temp_title.append(classify_word(GLOVE_OBJ,tw.lower()))
			print(tw,temp_title[-1])
		types.append([temp_title,title])
	return types
