import requests,random,json
import math,time
from modules.log import logger


headers=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12','Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0;Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3','Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.1 Mobile Safari/533.1','Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3']


def kongzhiqingqiu_quake(url,header1,data,domain):
	#对requests请求进行限制，避免未获取到数据的情况。
	i=0
	while i<3:
		try:
			res = requests.post(url=url, headers=header1, json=data, timeout=(10,10), verify=False)
			ret = json.loads(res.text)
			#print (ret)
			if ret["code"]==0 and res.status_code==200:
				return res
			else:
				logger.log('INFOR',"		quake查询{}错误，正在进行重试...".format(domain))
				i=i+1
		except:
			logger.log('INFOR',"		quake查询{}错误，正在进行重试...".format(domain))
			i=i+1
	logger.log('ERROR','quake 查询 {} 失败，即将返回空值。'.format(domain))
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
	response = kongzhiqingqiu_quake("https://quake.360.cn/api/v3/search/quake_service",header1,data,domain)
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
