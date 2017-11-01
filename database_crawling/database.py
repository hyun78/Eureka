#database crawling 

#로그인
#참고 블로그 : https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/
url_login = 'https://42matters.com/user/login'
method = 'post'
#input : email, passward, salt, anti_csrf_token,
#example 
# email:q@23
# password:qq
# salt:9wbqKZMxZ19te6s8D
# anti_csrf_token:7b5b0a3adbac5103ed08f0e9bdec1391a7ff30b1
with requests.Session() as s:
	url = 'https://42matters.com/app-market-explorer/android/?view=filter'
		res = s.get(url)
		data = res.json()['response']
			#name = email, name = password

