import requests,random,json,time
from modules.log import logger


headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']


def crt_sh_get(domain):
	url="https://crt.sh/?Identity={}&output=json".format(domain)
	header1=random.choice(headers)
	header1={'user-agent':header1}
	i=0
	while i<3:
		try:
			time.sleep(1)
			resp=requests.get(url=url, headers=header1,verify=False,timeout=(10,10))
			#print (resp.text)
			if resp.status_code==200:
				#print (resp.json())
				return resp.json()
			else:
				logger.log('INFOR',"		crt查询{}错误，正在进行重试...".format(domain))
				i=i+1
		except requests.exceptions.RequestException:
			logger.log('INFOR',"		crt查询{}错误，正在进行重试...".format(domain))
			i=i+1
	logger.log('ERROR','crt 查询 {} 失败，即将返回空值。'.format(domain))
	return []