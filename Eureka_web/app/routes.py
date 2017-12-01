from flask import Flask,render_template
from flask import request as req

import time
import os
from .main_routine import *
from .imgout import *

#######################
#   FLASK APP ROUTE   #
#######################

app = Flask(__name__)

@app.route('/')
def hello_world():
	sections = os.listdir('database')
	return render_template('home.html',sections=sections)

@app.route('/q')
def h2():
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
	dict_ = read_cluster('database/'+section+'/clustered_dictionary.json')
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
	type_statistics= read_type_statistics('database/'+section+'/type_statistics.json')
	# list of dictionary; type_statistics[i][j] : 고유어가 i개 들어간 j길이의 제목들의 통계 
	# type_statistics[i][j][typenum][0] : typenum으로 분류되는 제목들의 숫자
	type_distribution = generate_type_distribution(type_statistics,cwn)
	# iter_num : 몇개의 단어를 뽑을 것인가?
	iter_num = 100
	#word dict이 keyword : [word,typenumber,pos] 였다면 이건 typenum:[word1, word2, ...]인 dictonary
	type_word_dict = generate_type_word_dict(word_dict)
	res = generate_result(iter_num,type_word_dict,type_distribution)
	print(res)
	print(section)
	####
	res_send = {}
	res_send['names'] = res
	res_send['section'] = section
	make_img(section)
	make_wan_img(section,cwn)
	return render_template('result_page.html',value=res_send,img_name1=('templates/'+colorscheme+section+'_WANcencored.png'),img_name2=('templates/'+colorscheme+section+'.png'))

@app.route('/admin_page')
def admin_page_view():
	sections = os.listdir('database')
	return render_template('admin_page.html',sections=sections)

@app.route('/add_request/<string:selected_section_id>')
def admin_section_add(selected_section_id):
	print(selected_section_id)
	path = 'database/'+selected_section_id
	print(path)
	if not os.path.isdir(path):
		os.mkdir(path)
	else:
		print("not created!")
	sections = os.listdir('database')
	return render_template('admin_page.html',sections=sections)

@app.route('/flush_database_request')
def admin_database_flush():
	selected_section_id = req.args.get('selected_section_id')
	print(selected_section_id)
	path = 'database/'+selected_section_id
	setup_database(selected_section_id)
	sections = os.listdir('database')
	return render_template('admin_page.html',sections=sections)
	
