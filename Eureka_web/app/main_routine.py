##this is main routine file
from wan import search_WAN
def main():
	keyward_user = input("type keywords saperated by space")
	klst = keywords.split()
	n = len(klst)

	#genearte words set
	associated_words_set = search_WAN(klst)
	#associated_word_set[0] ~ associated_word_set[n-1] 
	#associated_word_set[i]['text'] = klst[i]
	#associated_word_set[i]['text'] = klst[i]'s associated words sorted by weight
	k = 10
	word_dict = {}
	for i in range(n):
		word_dict[associated_words_set[i]['text']]= []
		for wd in associated_words_set[i]['items'][:k]:
			temp = []
			temp.append(wd['item'])
			temp.append(classify_word(wd['item']))
			temp.append(wd['pos'])
			word_dict[associated_words_set[i]['text']].append(temp)
	keyword_lst = []
	for kw in klst:
		temp = []
		temp.append(kw)
		temp.append(classify_word(kw))
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
		type_dict[aw[1]] = 0

	avt = type_dict.keys() # 가능한 타입들 
	cwn = []
	for i in avt:
		for j in avt:
			cwn.append(str(i)+'_'+str(j)+'_2')
		cwn.append(str(i)+'_1')
	#cwn = ['1_3_2','2_4_2','1_1']

	type_distribution = {}
	total = 0
	for i in range(2):
		if (nump_pro ==1 and i ==1 ):
			break;
		for type_number in cwn:
			type_distirbution[type_number]= type_statistics[num_pro][2-i-num_pro][type_number]
			total+=type_statistics[num_pro][2-i-num_pro][type_number]
	
	for d in type_distribution:
		type_distribution[d] = type_distribution[d]/total
		cnt += type_distribution[d]/total
	p_ = list(type_distirbution.values())
	lsts_ = list(type_distribution.keys())
	type_distribution.values(lsts_[-1]) = type_distribution.values(lsts_[-1])+ (1 - sum(p_))
	p_ = list(type_distirbution.values())
	# iter_num
	iter_num = 10
	res = []
	type_word_dict = {}
	for we in word_dict
	for i in range(iter_num):
		randium_type = numpy.random.choice(lsts_, p=p_) 
		res.append(generate_type_with_words(randium_type,,keyword_lst))
	print(res)
	return res

def generate_type_with_words(type_no,word_set):
	#
	for we in word_set:
		word_set[we][1]



















