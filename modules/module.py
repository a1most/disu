import openpyxl
import os,re,requests,base64,configparser,json,random
from urllib import parse
import time,datetime
import math,time,sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

from modules.savedb import *
from modules.data_format import *
from modules.log import logger


from pm.fofa import *
from pm.hunter import *
from pm.crt import *
from pm.fullhunt import *
from pm.quake import *
from pm.shodan import *
from pm.virustotal import *
from pm.zoomeye import *
from pm.rapiddns import *
from pm.chaziyu import *
from pm.dnsscan import *
from pm.certspotter import *
from pm.threatminer import *


def getdata(domain,single=None):
	timestamp=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	path_excel=os.path.join(os.getcwd(), 'output', domain+"-"+timestamp+'.xlsx')
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

	rapiddnsdata123=rapiddns_get(domain)
	if rapiddnsdata123:
		rapiddnsdata=extend_rapiddns(rapiddnsdata123,domain)
		logger.log('INFOR',"	rapiddns获取到子域名数据{}条。".format(len(rapiddnsdata)))
	else:
		rapiddnsdata=[]
		logger.log('ERROR',"	rapiddns未获取到{}数据！".format(domain))
	
	#以上为rapiddns获取数据代码。

	chaziyudata123=chaziyu_get(domain)
	if chaziyudata123:
		chaziyudata=extend_chaziyu(chaziyudata123,domain)
		logger.log('INFOR',"	chaziyu获取到子域名数据{}条。".format(len(chaziyudata)))
	else:
		chaziyudata=[]
		logger.log('ERROR',"	chaziyu未获取到{}数据！".format(domain))
	#以上为chaziyu获取数据代码。

	dnsscandata123=dnsscan_get(domain)
	if dnsscandata123:
		dnsscandata=extend_dnsscan(dnsscandata123,domain)
		logger.log('INFOR',"	dnsscan获取到子域名数据{}条。".format(len(dnsscandata)))
	else:
		dnsscandata=[]
		logger.log('ERROR',"	dnsscan未获取到{}数据！".format(domain))
	#以上为dnsscan获取数据代码。

	certspotterdata123=certspotter_get(domain)
	#print (certspotterdata123)
	if certspotterdata123:
		certspotterdata=extend_certspotter(certspotterdata123,domain)
		logger.log('INFOR',"	certspotter获取到子域名数据{}条。".format(len(certspotterdata)))
	else:
		certspotterdata=[]
		logger.log('ERROR',"	certspotter未获取到{}数据！".format(domain))
	#以上为certspotter获取数据代码。

	threatminerdata123=threatminer_get(domain)
	if threatminerdata123:
		threatminerdata=extend_threatminer(threatminerdata123,domain)
		logger.log('INFOR',"	threatminer获取到子域名数据{}条。".format(len(threatminerdata)))
	else:
		threatminerdata=[]
		logger.log('ERROR',"	threatminer未获取到{}数据！".format(domain))
	#以上为threatminer获取数据代码。
	
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
	
	all_data_temp=crt_sh_data+virustotaldata+shodandata+fofadata+quakedata+fullhuntdata+zoomeyedata+rapiddnsdata+chaziyudata+dnsscandata+certspotterdata+threatminerdata+hunterdata
	#all_data_temp=hunterdata
	all_data=dr(all_data_temp)
	#调用dr函数进行去重。
	if all_data:
		logger.log('INFOR',"正在对子域名进行存活性探测，请耐心等候：")
		save_excel(all_data,path_excel)
		logger.log('INFOR',"完成存活性探测，数据已存储至：{}。".format(path_excel))
		savedb_data(all_data)
	else:
		logger.log('ERROR',"获取到{}的子域名信息为空，不进行存储操作。".format(domain))
	#在保存到excel的过程中进行去重。