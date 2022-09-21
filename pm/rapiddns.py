from modules.log import logger
import requests,random,json,base64,re
import math


headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']


def kongzhiqingqiu_rapiddns(url,header1,domain):
	#对requests请求进行限制，避免因网络问题未获取到数据的情况。
	i=0
	while i<3:
		res = requests.get(url=url, headers=header1, timeout=10, verify=False)
		if res.status_code==200:
			regx="<td>(.*?)"+domain+"</td>"
			total_pipei1=re.findall("Total:(.*?)</div>",res.text)
			total_pipei2=re.findall(">(.*?)<",str(total_pipei1))
			domain_pipei1=re.findall(regx,res.text)
			data=[]
			for i in domain_pipei1:
				domain_tmp=i+domain
				data.append(domain_tmp)
			return int(total_pipei2[0]),data
		else:
			i=i+1
def temp(total,data,domain,header1):
	rapiddns_data=[]
	rapiddns_data=rapiddns_data+data
	pages = total / 100
	pages = math.ceil(pages)
	if pages!=1:
		for page in range(2, pages + 1):
			url = "https://rapiddns.io/s/{}?page={}#result".format(domain,page)
			total_linshi,res = kongzhiqingqiu_rapiddns(url,header1,domain)
			rapiddns_data=rapiddns_data+res
		return rapiddns_data
	else:
		return rapiddns_data

def rapiddns_get(domain):
	header1=random.choice(headers)
	header1={'user-agent':header1}
	url="https://rapiddns.io/s/"+domain

	total,data= kongzhiqingqiu_rapiddns(url,header1,domain)
	rapiddns_data=temp(total,data,domain,header1)
	return rapiddns_data