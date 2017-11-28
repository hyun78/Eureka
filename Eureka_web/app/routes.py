from flask import Flask,render_template
from flask import request as req
import time

from .main_routine import *


#######################
#   FLASK APP ROUTE   #
#######################

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/search/<string:keywords>')
def hello_world2(keywords):

    return "THIS IS RESULT"
@app.route('/result')
def test():
	keyword_user = req.args.get('keys')
	section = req.args.get('selected_section')
	klst = keyword_user.split()
	n = len(klst)

	#genearte words set
	associated_words_set = search_WAN(klst)
	#associated_word_set[0] ~ associated_words_set[n-1] 
	#associated_word_set[i]['text'] = klst[i]
	#associated_word_set[i]['text'] = klst[i]'s associated words sorted by weight
	k = 20
	dict_ = read_cluster('database/'+section+'/clustered_dictionary_'+section+'.json')
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
	type_statistics= read_type_statistics('database/'+section+'/type_statistics_'+section+'.json')
	type_distribution = generate_type_distribution(type_statistics,cwn)
	# iter_num
	iter_num = 100
	type_word_dict = generate_type_word_dict(word_dict)
	res = generate_result(iter_num,type_word_dict,type_distribution)
	print(res)
	print(section)
	####
	res_send = {}
	res_send['names'] = res
	res_send['section'] = section
	return render_template('result_page.html',value=res_send)