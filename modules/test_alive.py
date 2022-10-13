import requests

def check_alive(url):
	if 'http://' not in url and 'https://' not in url:
		#print (url)
		url1="http://"+str(url)+"/"
		url2="https://"+str(url)+"/"
		#print (url1,url2)
		try:
			r1=requests.get(url1,timeout=5)
		except Exception as e:
			r1=0
		try:
			r2=requests.get(url2,timeout=5,verify=False)
		except Exception as e:
			r2=0
		if r1!=0:
			return "存活",'http',r1.status_code,r1.headers.get('Content-Length')
		if r2!=0:
			return "存活",'https',r2.status_code,r2.headers.get('Content-Length')
		if r1==0 and r2==0:
			return "不存活",'','',''
	if 'http://' in url:
		try:
			r3=requests.get(url,timeout=5)
		except Exception as e:
			r3=0
		if r3!=0:
			return '存活','http',r3.status_code,r3.headers.get('Content-Length')
		if r3==0:
			return "不存活",'','',''
	if 'https://' in url:
		try:
			r4=requests.get(url,timeout=5,verify=False)
		except Exception as e:
			r4=0
		if r4!=0:
			return '存活','https',r4.status_code,r4.headers.get('Content-Length')
		if r4==0:
			return "不存活",'','',''
