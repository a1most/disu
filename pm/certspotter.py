#https://api.certspotter.com/v1/issuances?domain=baidu.com&include_subdomains=true&expand=dns_names


import requests,random,json
from modules.log import logger
from modules.data_format import dr

headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']

def kongzhiqingqiu_certspotter(url,header1,domain):
	#对requests请求进行限制，避免因网络问题未获取到数据的情况。
	#print ("aaaaaaaaa")
	i=0
	while i<3:
		try:
			res = requests.get(url=url, headers=header1, timeout=(10,10), verify=False)
			ret = json.loads(res.text)
			#print (res.status_code)
			if res.status_code==200 and len(ret)!=0:
				return ret
			else:
				logger.log('INFOR',"		certspotter查询{}失败，正在进行重试...".format(domain))
				i=i+1
		except Exception as e:
			logger.log('INFOR',"		certspotter查询{}失败，正在进行重试...".format(domain))
			i=i+1
	logger.log('ERROR','certspotter 查询 {} 失败，即将返回空值。'.format(domain))
	return []
def geshihua(data,domain):
	temp=[]
	for i in data:
		if domain not in i:
			continue
		if "*." in i:
			i=i.replace("*.","www.")
		if i not in temp:
			temp.append(i)
	#print (temp)
	return temp


def certspotter_get(domain):
	domains=[]
	header1=random.choice(headers)
	header1={'user-agent':header1}
	url="https://api.certspotter.com/v1/issuances?domain={}&include_subdomains=true&expand=dns_names".format(domain)
	try:
		resp=kongzhiqingqiu_certspotter(url,header1,domain)
		for i in resp:
			#domains=i['dns_names']
			domains=domains+i['dns_names']
		data=geshihua(domains,domain)
		#return(data)
	except:
		logger.log('ERROR','certspotter 查询{}:{}'.format(domain,e.args))
		data=[]
	return data