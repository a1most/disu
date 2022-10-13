#https://chaziyu.com/ipchaxun.do?domain=baidu.com&page=2
#https://chaziyu.com/zhaokuaizhao.do?domain=baidu.com&page=2
#https://chaziyu.com/baidu.com
import requests,random,json,time
import re
from modules.log import logger

headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']


def kongzhiqingqiu_chaziyu(url,domain,header1):
	ip=str(random.randint(1,254))+'.'+str(random.randint(1,254))+'.'+str(random.randint(1,254))+'.'+str(random.randint(1,254))
	header1['Cdn-Src-Ip']=ip
	i=0
	while i<3:
		try:
			res = requests.get(url=url, headers=header1, timeout=(10,10), verify=False)
			return res
		except:
			logger.log('INFOR',"		chaziyu正在对{}进行重试中：".format(domain))
			i=i+1
		time.sleep(1)
	logger.log('ERROR','chaziyu 查询 {} 失败，即将返回空值。'.format(domain))
	return []

def chaziyu(domain,header1):
	domains=[]
	url1="https://chaziyu.com/{}".format(domain)
	response=kongzhiqingqiu_chaziyu(url1,domain,header1)
	try:
		temp=re.findall('target="_blank">(.*?)</a>',response.text)
		for i in temp:
			if domain in i and i not in domains:
				domains.append(i)
	except:
		logger.log('ERROR','chaziyu 查询{}:{}'.format(domain,e.args))
		domains=[]
	return domains


def ipchaxun(domain,header1):
	ipchaxun_data=[]
	for i in range(2,21):
		url="https://chaziyu.com/ipchaxun.do?domain={}&page={}".format(domain,i)
		response=kongzhiqingqiu_chaziyu(url,domain,header1)
		try:
			ret = json.loads(response.text)
			data=ret['data']
			result=data['result']
		except:
			result=[]
		ipchaxun_data=ipchaxun_data+result
		#print (ipchaxun_data)
		if len(result)==0:
			#print ('111111')
			break
	return ipchaxun_data

def zhaokuaizhao(domain,header1):
	zhaokuaizhao_data=[]
	for i in range(2,21):
		url="https://chaziyu.com/zhaokuaizhao.do?domain={}&page={}".format(domain,i)
		response=kongzhiqingqiu_chaziyu(url,domain,header1)
		try:
			ret = json.loads(response.text)
			data=ret['data']
			result=data['result']
		except:
			result=[]
		zhaokuaizhao_data=zhaokuaizhao_data+result
		if len(result)==0:
			#print ('111111')
			break
	return zhaokuaizhao_data

def chaziyu_get(domain):
	header1=random.choice(headers)
	header1={'user-agent':header1}
	chaziyu_data123=chaziyu(domain,header1)
	if len(chaziyu_data123)==0:
		chaziyu_data=[]
	else:
		chaziyu_data=chaziyu_data123
	ipchaxun_data123=ipchaxun(domain,header1)
	if len(ipchaxun_data123)==0:
		ipchaxun_data=[]
	else:
		ipchaxun_data=ipchaxun_data123
	zhaokuaizhao_data123=zhaokuaizhao(domain,header1)
	if len(zhaokuaizhao_data123)==0:
		zhaokuaizhao_data=[]
	else:
		zhaokuaizhao_data=zhaokuaizhao_data123
	all_data=chaziyu_data+ipchaxun_data+zhaokuaizhao_data
	return all_data