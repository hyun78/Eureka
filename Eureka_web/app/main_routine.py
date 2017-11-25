##this is main routine file
from wan import search_WAN
from word_classification import *
import numpy,random
def main():
	keyword_user = input("type keywords saperated by space\n")
	#klst = keyword_user.split()
	#keyword_user = "amazon tiger jungle"
	klst = keyword_user.split()
	n = len(klst)

	#genearte words set
	associated_words_set = search_WAN(klst)
	#associated_word_set[0] ~ associated_words_set[n-1] 
	#associated_word_set[i]['text'] = klst[i]
	#associated_word_set[i]['text'] = klst[i]'s associated words sorted by weight
	k = 20
	dict_ = read_cluster('clustered_dictionary.json')
	word_dict = generate_word_dict(n,associated_words_set,k,dict_)
	keyword_lst = []

	for kw in klst:
		temp = []
		temp.append(kw)
		temp.append(classify_word_type2(kw,dict_))
		keyword_lst.append(temp)

	#word dict = { keyword : [  [associated word1,type,pos]     ] }
	#keyword dict = [ [keyword, type] ] 

	#combine start
	#type statistics [number of 고유명사] [ title length - number of 고유명사 ] 
	num_pro = 0  #user input value
	#     type_statistics[0][2]
	# input : n keyword , and each k related word ; nk word
	# output : O(nk*nk)
	type_dict = {}
	for aw in word_dict:
		for te in word_dict[aw]:
			type_dict[te[1]] = 0
	avt = type_dict.keys() # 가능한 타입들 
	
	cwn = []
	for i in avt:
		for j in avt:
			cwn.append(str(i)+'_'+str(j)+'_2')
		cwn.append(str(i)+'_1')
	#cwn = ['1_3_2','2_4_2','1_1']
	type_statistics= read_type_statistics('type_statistics.json')

	type_distribution = generate_type_distribution(num_pro,type_statistics,cwn)
	# iter_num
	iter_num = 100
	
	type_word_dict = generate_type_word_dict(word_dict)
	
	res = generate_result(iter_num,type_word_dict,type_distribution)
	#print(res)
	return res
def read_type_statistics(filename):
	t = None
	with open(filename) as f:
		t = json.load(f,object_pairs_hook=dict)
	return t
def generate_word_dict(n,associated_words_set,k,dict_):
	word_dict = {}
	for i in range(n):
		word_dict[associated_words_set[i]['text']]= []
		for wd in associated_words_set[i]['items'][:k]:
			temp = []
			temp.append(wd['item'])
			temp.append(classify_word_type2(wd['item'].lower(),dict_))
			temp.append(wd['pos'])
			word_dict[associated_words_set[i]['text']].append(temp)
	return word_dict


def generate_type_distribution(num_pro,type_statistics,cwn):
	type_distribution = {}
	total = 0
	
	for type_number in cwn:
		len_ = int(type_number[-1])
		try:
			type_distribution[type_number]= type_statistics[num_pro][len_][type_number][0]
			
			total+=type_statistics[num_pro][len_][type_number][0]
			
		except:
			type_distribution[type_number]= 0
	
	for d in type_distribution:
		type_distribution[d] = type_distribution[d]/total
		#cnt += type_distribution[d]/total
	return type_distribution
def generate_type_word_dict(word_dict):
	type_word_dict = {}
	for we in word_dict.values():
		for w in we:
			try:
				type_word_dict[w[1]].append(w[0])
			except:
				type_word_dict[w[1]] = [w[0]]
	return type_word_dict
def generate_type_with_words(type_no,type_word_dict):
	type_split = type_no.split('_')
	type_len = int(type_split[-1]) # 10_1_2
	res = []
	for i in range(type_len):
		res.append(random.choice(type_word_dict[int(type_split[i])]))
	res = ' '.join(res)
	return res
def generate_result(iter_num,type_word_dict,type_distribution):
	res = []
	p_ = list(type_distribution.values())
	lsts_ = list(type_distribution.keys())
	type_distribution[lsts_[-1]] = type_distribution[lsts_[-1]]+ (1 - sum(p_))
	p_ = list(type_distribution.values())
	for i in range(iter_num):
		randium_type = numpy.random.choice(lsts_, p=p_) 
		res.append([generate_type_with_words(randium_type,type_word_dict),randium_type])
	return res



















