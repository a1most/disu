import openpyxl
import os,re,requests,base64,configparser,json,random
from urllib import parse
import time,datetime
import shodan
from modules.savedb import *
from modules.data_format import *
from modules.log import logger
import math,time

headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']

def fofa_get(domain,fofa_mail,fofa_key):
	header1=random.choice(headers)
	header1={'user-agent':header1}
	#print (header1)
	#headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	domain=str(base64.b64encode(domain.encode(encoding='utf-8')), 'utf-8')
	url=r"https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}".format(fofa_mail,fofa_key,domain)
	i=0
	while i<3:
		try:
			rsp=json.loads(requests.get(url=url, headers=header1, timeout=10, verify=False).text)
			try:
				asb=rsp['results']
				#print (rsp)
				return asb
			except:
				return []
		except requests.exceptions.RequestException as e:
			logger.log('ERROR', e.args)
			i=i+1
	#f.write('\r\n')

def kongzhiqingqiu(url,header1):
	#对requests请求进行限制，避免未获取到数据的情况。
	i=0
	while i<3:
		res = requests.get(url=url, headers=header1, timeout=10, verify=False)
		ret = json.loads(res.text)
		data = ret["data"]
		#print (data)
		if ret["code"]==200 and data:
			return res
		else:
			i=i+1
			#print (i)

def hunter_get(domain,hunter_key):
	qianxin_Results = []
	header1=random.choice(headers)
	header1={'user-agent':header1}
	qbase64 = str(base64.b64encode(domain.encode(encoding='utf-8')), 'utf-8')
	# 第n页
	page = 1
	# 每页的数据量
	size = 100
	# 只看Web资产
	is_web = 1
	# 状态码200
	status_code = 200
	# 现在时间
	end_time = datetime.datetime.now()
	# 一年前时间
	start_time = str(int(end_time.strftime("%Y")) - 1) + "-" + end_time.strftime("%m-%d %H:%M:%S")
	# url编码
	end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
	start_time = parse.quote(start_time)
	end_time = parse.quote(end_time)


	url = "https://hunter.qianxin.com/openApi/search?api-key={}&search={}&page={}&page_size={}&is_web={}&status_code={}&start_time={}&end_time={}".format(
		hunter_key, qbase64, page, size, is_web, status_code, start_time, end_time
	)

	try:
		res=kongzhiqingqiu(url,header1)
		ret = json.loads(res.text)
		#print (ret)
		if ret["code"] == 401:
			return []

		data = ret["data"]
		# 查询的总共数量
		total = data["total"]

		pages = total / size
		pages = math.ceil(pages)

		arr = data["arr"]
		qianxin_Results_tmp=arr
		qianxin_Results.extend(qianxin_Results_tmp)
		#print (qianxin_Results)


		if pages != 1:
			for page in range(2, pages + 1):
				#print("[qianxin] page{}".format(page))
				url = "https://hunter.qianxin.com/openApi/search?api-key={}&search={}&page={}&page_size={}&is_web={}&status_code={}&start_time={}&end_time={}".format(
					hunter_key, qbase64, page, size, is_web, status_code, start_time, end_time
				)
				res = kongzhiqingqiu(url,header1)
				ret = json.loads(res.text)
				#print (ret)
				data = ret["data"]
				arr = data["arr"]
				#print (arr)
				qianxin_Results_tmp=arr
				qianxin_Results.extend(qianxin_Results_tmp)
		return qianxin_Results
	except Exception as e:
		logger.log('ERROR','qianxin 查询 {} : {}'.format(domain, e.args))
		return []
def kongzhiqingqiu_quake(url,header1,data):
	#对requests请求进行限制，避免未获取到数据的情况。
	i=0
	while i<3:
		try:
			res = requests.post(url=url, headers=header1, json=data, timeout=20, verify=False)
			ret = json.loads(res.text)
			#print (ret)
			if ret["code"]==0 and res.status_code==200:
				return res
		except:
			#print (i)
			i=i+1
	return []

def quake_get(domain,quake_key):
	header1=random.choice(headers)
	header1={'user-agent':header1}
	header1['X-QuakeToken']=quake_key
	data = {
	"query": "domain: "+domain,
	"start": 0,
	"size": 500
	}
	response = kongzhiqingqiu_quake("https://quake.360.cn/api/v3/search/quake_service",header1,data)
	if response:
		ret=response.json()
		if ret['code']=='q3005':
			logger.log('ERROR',"	调用360quakeapi过于频繁，请稍后重试。")
			return []
		elif ret['code']=='q3007':
			logger.log('ERROR',"	当前360quakeapi对应用户的积分不足，请更新api信息。")
			return []
		elif ret['code']=='q3011':
			logger.log('ERROR',"	360quake用户缺少必要权限，请联系管理员 quake@360.cn。")
			return []
		elif ret['code']=='q3017':
			logger.log('ERROR',"	360quake暂不支持该字段查询。")
			return []
		elif ret['code']==0:
			data=ret['data']
			return data
		else:
			logger.log('ERROR',"	360quake其他错误，请重试。")
			return []
	else:
		return []


def shodan_get(domain,shodan_key):
	#domain="domain="
	api=shodan.Shodan(shodan_key)
	results=api.search(domain)
	shodan_data_all=[]
	for i in results['matches']:
		shodan_data=[]
		shodan_data.append(i['hostnames'])
		shodan_data.append(i['ip_str'])
		shodan_data.append(i['port'])
		shodan_data.append('shodan')
		shodan_data.append(domain)
		shodan_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		shodan_data_all.append(shodan_data)
	return shodan_data_all

def virustotal_get(domain,virustotal_key):
	url="https://www.virustotal.com/vtapi/v2/domain/report?domain={}&apikey={}".format(domain,virustotal_key)
	header1=random.choice(headers)
	header1={'user-agent':header1}
	i=0
	while i<3:
		try:
			response = requests.get(url=url, headers=header1,verify=False,timeout=5)
			if response.status_code==403:
				logger.log('ERROR',"	VirusTotal api 错误.")
				return []
			elif response.status_code==200:
				ret=response.json()
				if 'subdomains' in ret.keys():
					virustotal_domains=ret['subdomains']
					return virustotal_domains
			else:
				logger.log('ERROR','	VirusTotal API No Subdomains.')
				return []
		except requests.exceptions.RequestException:
			i=i+1
def fullhunt_get(domain,fullhunt_key):
	url="https://fullhunt.io/api/v1/domain/{}/subdomains".format(domain)
	header1=random.choice(headers)
	header1={'user-agent':header1}
	header1['X-API-KEY']=fullhunt_key
	i=0
	while i<3:
		try:
			response=requests.get(url=url, headers=header1,verify=False,timeout=20)
			if response.status_code==403:
				logger.log('ERROR',"	fullhunt禁止请求的资源。")
				return []
			elif response.status_code==401:
				logger.log('ERROR',"	fullhuntAPI或者KEY出现错误。")
				return []
			elif response.status_code==429:
				logger.log('ERROR',"	fullhunt请求次数过多。")
				return []
			elif response.status_code==200:
				ret=response.json()
				#print (ret)
				return ret
			else:
				logger.log('ERROR','	fullhunt No Subdomains.')
				return []
		except requests.exceptions.RequestException:
			i=i+1
def crt_sh_get(domain):
	url="https://crt.sh/?Identity={}&output=json".format(domain)
	header1=random.choice(headers)
	header1={'user-agent':header1}
	i=0
	while i<3:
		try:
			time.sleep(1)
			resp=requests.get(url=url, headers=header1,verify=False,timeout=10)
			if resp.status_code==200:
				#print (resp.json())
				return resp.json()
			else:
				logger.log('ERROR',"	crt.sh获取数据出错。")
				#print (resp.text)
				return []
		except requests.exceptions.RequestException:
			i=i+1
def kongzhiqingqiu_zoomeye(url,header1):
	#对requests请求进行限制，避免因网络问题未获取到数据的情况。
	i=0
	while i<3:
		res = requests.get(url=url, headers=header1, timeout=10, verify=False)
		ret = json.loads(res.text)
		#print (data)
		if res.status_code==200:
			return res
		else:
			i=i+1

def zoomeye_get(domain,zoomeye_key):
	zoomeye_results=[]
	header1=random.choice(headers)
	header1={'user-agent':header1}
	header1['API-KEY']=zoomeye_key
	url="https://api.zoomeye.org/domain/search?q={}&type=0&page=1".format(domain)
	try:
		res=kongzhiqingqiu_zoomeye(url,header1)
		ret=res.json()
		data=ret['list']
		total=ret['total']
		pages=total/(len(data))
		pages=math.ceil(pages)
		zoomeye_results.extend(data)
		if pages!=1:
			for page in range(2,pages+1):
				url="https://api.zoomeye.org/domain/search?q={}&type=0&page={}".format(domain,page)
				res=kongzhiqingqiu_zoomeye(url,header1)
				ret=res.json()
				data=ret['list']
				zoomeye_results.extend(data)
		return zoomeye_results
	except Exception as e:
		logger.log('ERROR','zoomeye 查询{}:{}'.format(domain,e.args))
		return []


def getdata(domain,single=None):
	timestamp=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	path_excel=os.getcwd()+'\\output\\'+domain+"-"+timestamp+'.xlsx'
	conf=configparser.ConfigParser()
	conf.read('./config.ini')
	sections=conf.sections()
	logger.log('INFOR',"正在开始获取{}的子域名信息：".format(domain))

	crt_sh_data123=crt_sh_get(domain)
	if crt_sh_data123:
		crt_sh_data=extend_crt_sh(crt_sh_data123,domain)
		logger.log('INFOR',"	crt.sh获取到子域名数据{}条。".format(len(crt_sh_data)))
	else:
		#print (crt_sh_data123)
		crt_sh_data=[]
		logger.log('ERROR',"	crt.sh未获取到{}数据！".format(domain))
	#以上为crtsh获取数据代码
	
	fullhunt_key=conf.get('fullhunt_api','key')
	if fullhunt_key:
		fullhuntdata123=fullhunt_get(domain,fullhunt_key)
		if fullhuntdata123:
			fullhuntdata=extend_fullhunt(fullhuntdata123,domain)
			logger.log('INFOR',"	fullhunt获取到子域名数据{}条。".format(len(fullhuntdata)))
			#print (fullhuntdata)
		else:
			fullhuntdata=[]
			logger.log('ERROR',"未获取到数据或者fullhunt次数不够！")
	else:
		fullhuntdata=[]
		logger.log('ERROR',"未获取到fullhunt_key值，请前往config.ini文件进行补充或忽略此信息。")
	#以上为fullhunt获取数据代码。
	
	shodan_key=conf.get('shodan_api','key')
	if shodan_key:
		shodandata=shodan_get(domain,shodan_key)
		logger.log('INFOR',"	shodan获取到子域名数据{}条。".format(len(shodandata)))
	else:
		shodandata=[]
		logger.log('ERROR',"未获取到shodan_key值，请前往config.ini文件进行补充或忽略此信息。")
	#以上为shodan获取数据代码,调用shodan库，直接获取。


	quake_key=conf.get('quake_api','key')
	if quake_key:
		quake123=quake_get(domain,quake_key)
		if quake123:
			quakedata=extend_quake(quake123,domain)
			logger.log('INFOR',"	360quake获取到子域名数据{}条。".format(len(quakedata)))
			#print (quakedata)
		else:
			quakedata=[]
			logger.log('ERROR',"未获取到数据或者quake积分不够！")
	else:
		quakedata=[]
		logger.log('ERROR',"未获取到quake_key值，请前往config.ini文件进行补充或忽略此信息。")
	#以上为quake获取数据代码。

	fofa_email=conf.get('fofa_api','email')
	fofa_key=conf.get('fofa_api','key')
	if fofa_email and fofa_key:
		fofadata123=fofa_get(domain,fofa_email,fofa_key)
		#print (fofadata123)
		if fofadata123:
			fofadata=extend_fofa(fofadata123,domain)
			logger.log('INFOR',"	fofa获取到子域名数据{}条。".format(len(fofadata)))
			#print (fofadata)
		else:
			fofadata=[]
			logger.log('ERROR',"未获取到数据或者fofa积分不够！")
	else:
		fofadata=[]
		logger.log('ERROR',"未获取到fofa_email或fofa_key值，请前往config.ini文件进行补充或忽略此信息。")
	#以上为fofa获取数据代码。

	hunter_key=conf.get('hunter_api','key')
	if hunter_key:
		hunter123=hunter_get(domain,hunter_key)
		if hunter123:
			#print ("aaaaaaaaaaaaa")
			hunterdata=extend_hunter(hunter123,domain)
			logger.log('INFOR',"	奇安信hunter获取到子域名数据{}条。".format(len(hunterdata)))
			#print (hunterdata)
		else:
			hunterdata=[]
			logger.log('ERROR',"	未获取到数据或者hunter积分不够！")
	else:
		hunterdata=[]
		logger.log('ERROR',"未获取到hunter_key值，请前往config.ini文件进行补充或忽略此信息。")
	#以上为hunter获取数据代码。
	
	virustotal_key=conf.get('virustotal_api','key')
	if virustotal_key:
		virustotaldata123=virustotal_get(domain,virustotal_key)
		if virustotaldata123:
			virustotaldata=extend_virustotal(virustotaldata123,domain)
			logger.log('INFOR',"	virustotal获取到子域名数据{}条。".format(len(virustotaldata)))
		else:
			virustotaldata=[]
			logger.log('ERROR',"未获取到数据或者virustotal积分不够！")
	else:
		virustotaldata=[]
		logger.log('ERROR',"未获取到virustotal_key值，请前往config.ini文件进行补充或忽略此信息。")
	#以上为virustotal获取数据代码。
	
	zoomeye_key=conf.get('zoomeye_api','key')
	if zoomeye_key:
		zoomeyedata123=zoomeye_get(domain,zoomeye_key)
		#print (zoomeyedata123)
		if zoomeyedata123:
			zoomeyedata=extend_zoomeye(zoomeyedata123,domain)
			#print (zoomeyedata)
			logger.log('INFOR',"	zoomeye获取到子域名数据{}条。".format(len(zoomeyedata)))
		else:
			zoomeyedata=[]
			logger.log('ERROR',"未获取到数据或者zoomeye积分不够！")
	else:
		zoomeyedata=[]
		logger.log('ERROR',"未获取到zoomeye_key值，请前往config.ini文件进行补充或忽略此信息。")

	all_data=crt_sh_data+virustotaldata+shodandata+quakedata+fofadata+hunterdata+fullhuntdata+zoomeyedata
	if all_data:
		logger.log('INFOR',"正在对子域名进行存活性探测，请耐心等候：")
		save_excel(all_data,path_excel)
		logger.log('INFOR',"完成存活性探测，数据已存储至：{}。".format(path_excel))
		savedb_data(all_data)
	else:
		logger.log('ERROR',"获取到{}的子域名信息为空，不进行存储操作。".format(domain))
	#在保存到excel的过程中进行去重。