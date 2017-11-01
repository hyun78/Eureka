#database crawling 
import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
import requests

#로그인
#참고 블로그 : https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/
#input : email, passward, salt, anti_csrf_token,
#example 
# email:q@23
# password:qq
# salt:9wbqKZMxZ19te6s8D
# anti_csrf_token:7b5b0a3adbac5103ed08f0e9bdec1391a7ff30b1

with requests.Session() as s:
#1 login page get
s = requests.Session
url_login = 'https://42matters.com/user/login'
request = urllib.request.Request(url_login) 
data = urllib.request.urlopen(request).read().decode() #UTF-8 encode
bs = BeautifulSoup(data,'lxml')
ent = bs.find_all('input')

#2 login post 

method = 'post'
email_id = 'seguakwa@gmail.com'
pwd = 'cs408'
salt_ = ent[2]['value']
_csrf = ent[3]['value']
params = {
	'email':email_id,
	'password' : pwd,
	'salt': salt_,
	'anti_csrf_token': _csrf
}
login_req = s.post(url_login, data=params)
print(login_req)
#3 crawling page get
url = 'https://42matters.com/app-market-explorer/android/?view=filter'
res = s.get(url)
bs = BeautifulSoup(data,'lxml')
		#name = email, name = password

