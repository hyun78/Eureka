from flask import Flask,render_template
from flask import request as req
import time

from . import wan 


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
	time.sleep(3)
	input_data = req.args.get('keys')
	print(input_data)
	keywords_list = input_data.split(" ")
	keywords_list = [x for x in keywords_list if not len(x)==0]
	translated_list = []
	for token in keywords_list:
		translated_list +=wan.translate(token)
	print("translated list",translated_list)
	query_string = ' '.join(translated_list)
	print("query string : ",query_string)
	#using WAN search with query_string
	#WAN_result = wan.search_WAN(query_string) 
	
	# translate result into korean words
	
	#make data tuple; (eng_word,korean_pronunciation,kor_word)

	# combine

	# evaluating

	# parsing data

	#rendering 
	return render_template('result_page.html')