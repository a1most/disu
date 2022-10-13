from modules.log import logger
import requests,random,json,base64,re
import math,time

headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']

#https://www.dnsscan.cn/dns.html


def kongzhiqingqiu_dnsscan(url,domain,header1,data):
	i=0
	while i<3:
		try:
			res = requests.post(url=url, headers=header1, data=data, timeout=(10,10), verify=False)
			#print (data)
			#print (res.text)
			if res.status_code==200 and "404 Not Found" not in res.text:
				return res
			else:
				logger.log('INFOR',"		dnsscan查询{}错误，正在进行重试...".format(domain))
				i=i+1
		except Exception as e:
			logger.log('INFOR',"		dnsscan查询{}错误，正在进行重试...".format(domain))
			i=i+1
	logger.log('ERROR','	dnsscan 查询 {} 失败，即将返回空值。'.format(domain))
	return []

def dnsscan_get(domain):
	temp=[]
	header1=random.choice(headers)
	header1={'user-agent':header1}
	header1['Content-Type'] = 'application/x-www-form-urlencoded'
	url="https://www.dnsscan.cn/dns.html"

	data = r'ecmsfrom=36.36.211.23&show=%e5%b9%bf%e4%b8%9c%e7%9c%81&num=&classid=0&keywords={}&page=1'.format(domain)       # 数据包
	resp=kongzhiqingqiu_dnsscan(url,domain,header1,data)
	try:
		domain_pipei1=re.findall(r'rel="nofollow" target="_blank">(.*?)</a></td>',resp.text)
		temp=temp+domain_pipei1
		total_pipei1=re.findall(r'查询结果为:([\d]+)条',resp.text)
	
		#print (domain_pipei1)
		#print (total_pipei1[0])

		pages=int(total_pipei1[0])/20
		pages = math.ceil(pages)
		if pages>1:
			for i in range(2,pages+1):
				url2="https://www.dnsscan.cn/dns.html?keywords={}&page={}".format(domain,i)
				resp2=kongzhiqingqiu_dnsscan(url2,domain,header1,data)
				domain_pipei2=re.findall(r'rel="nofollow" target="_blank">(.*?)</a></td>',resp.text)
				temp=domain_pipei2+temp
		return temp
	except:
		return temp


