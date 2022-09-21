import requests,random,json,base64
import math,time,datetime
from modules import log
from urllib import parse


headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']


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