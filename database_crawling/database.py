#database crawling 
import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import requests
import json
import time
#로그인
#참고 블로그 : https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/
#input : email, passward, salt, anti_csrf_token,
#example 
# email:q@23
# password:qq
# salt:9wbqKZMxZ19te6s8D
# anti_csrf_token:7b5b0a3adbac5103ed08f0e9bdec1391a7ff30b1
AUTH_TOKEN = '0bad9f919afadcea38e5ac14c655c5a9e2ff070d'


def get_data(category,start,limit):
	url = 'https://data.42matters.com/api/v2.0/android/apps/query.json'
	query = { 
		"access_token": AUTH_TOKEN,
		"fields":['title'],
		"limit": limit,
		"query": 
			{ "query_params": 
				{
				"from": start,
				"cat_keys":[category]
				}
			}

		}
	req = urllib.request.Request(url)
	req.add_header('Content-Type', 'application/json')
	data = urllib.request.urlopen(req,json.dumps(query).encode()).read().decode() #UTF-8 encode
	result = json.loads(data)

	return result
def data_savefile(filename,start,end):
	limit = 100
	category = 'GAME_ARCADE'
	res = get_data(category,start,limit)
	collection = []

	while (res['has_next'] and start<end):
		start += limit
		collection+=res['results']
		res = get_data(category,start,limit)
		time.sleep(1)
		print("try : ",start-limit," ~ ",start)

	total = {}
	total['items'] = collection
	make_json_file(filename,collection)
	return total
def make_json_file(filename,orderd_dict):
	with open(filename, 'w', encoding="utf-8") as make_file:
		json.dump(orderd_dict, make_file, ensure_ascii=False, indent="\t")
	return
#https://42matters.com/api/v2.0/android/ame/query.json?access_token=0bad9f919afadcea38e5ac14c655c5a9e2ff070d&cat_keys=GAME_ARCADE&fields=title,icon_72,market_url,package_name,category,developer,downloads,email,rating,sdks,website&from=40&full_text_search_flag=&full_text_search_in=title&full_text_term=&num=40&platform=android&sort=score&sort_order=asc
def check_api_status():
	url2 = 'https://data.42matters.com/api/v2.0/account.json'
	query_2 = {"access_token":AUTH_TOKEN}
	request = urllib.request.Request(url2) 
	data = urllib.request.urlopen(request,json.dumps(query).encode()).read().decode() #UTF-8 encode
	bs = BeautifulSoup(data,'lxml')
	return 
#query['access_token'] = AUTH_TOKEN
#res = s.post(url,data=query)
"""
https://42matters.com/api/v2.0/android/ame/query.json?access_token=0bad9f919afadcea38e5ac14c655c5a9e2ff070d&fields=title,icon_72,market_url,package_name,category,developer,downloads,email,rating,sdks,website&from=40&full_text_search_flag=&full_text_search_in=title&full_text_search_in=developer_name&num=40&platform=android&sort=score&sort_order=asc

"""
# with requests.Session() as s:
# #1 login page get
# s = requests.Session()
# url_login = 'https://42matters.com/user/login'
# request = urllib.request.Request(url_login) 
# data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
# bs = BeautifulSoup(data,'lxml')
# ent = bs.find_all('input')

# #2 login post 

# method = 'post'
# email_id = 'segaukwa@gmail.com'
# pwd = 'cs408'
# salt_ = ent[2]['value']
# _csrf = ent[3]['value']
# params = {
# 	'email':email_id,
# 	'password' : pwd,
# 	'salt': salt_,
# 	'anti_csrf_token': _csrf
# }
# login_req = s.post(url_login, data=params)
# print(login_req)
# #3 crawling page get
# url = 'https://42matters.com/app-market-explorer/android/?view=filter'
# res = s.get(url)
# bs = BeautifulSoup(data,'lxml')
# 		#name = email, name = password

# #query = json.loads(json.dumps(query))
# url = 'https://data.42matters.com/api/v2.0/android/apps/query.json?access_token=0bad9f919afadcea38e5ac14c655c5a9e2ff070d&fields=trackId,trackCensoredName'
