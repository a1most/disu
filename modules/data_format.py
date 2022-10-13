import time,openpyxl
from modules.log import logger
from modules.test_alive import check_alive
from tqdm import tqdm
import math

#格式化几个搜索引擎的数据，方便存储。

def dr(data):
	temp1=[]
	temp2=[]
	for i in data:
		if i[0] not in temp1:
			temp1.append(i[0])
			temp2.append(i)
	return temp2


#dr为去重函数。

def extend_hunter(hunterdata,domain):
	#print (type(hunterdata))
	hunter_data=[]
	for i in hunterdata:
		hunter_data2=[]
		hunter_data2.append(str(i['domain']))
		hunter_data2.append(i['ip'])
		hunter_data2.append(i['port'])
		hunter_data2.append('hunter')
		hunter_data2.append(domain)
		hunter_data2.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		hunter_data.append(hunter_data2)
	return hunter_data
def extend_fofa(fofadata,domain):
	fofa_data=[]
	for i in fofadata:
		i.append("fofa")
		i.append(domain)
		i.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		fofa_data.append(i)
	return fofa_data

def extend_quake(data,sin_domain):
	quake_data_all=[]
	for i in data:
		#service=i['service']
		quake_data=[]
		port=i['port']
		ip=i['ip']
		quake_domain=i['service']['http']['host']
		quake_data.append(quake_domain)
		quake_data.append(ip)
		quake_data.append(port)
		quake_data.append('360quake')
		quake_data.append(sin_domain)
		quake_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		quake_data_all.append(quake_data)
	return quake_data_all
def extend_virustotal(data,domain):
	virustotal_data_all=[]
	for i in data:
		virustotal_data=[]
		virustotal_data.append(i)
		virustotal_data.append('')
		virustotal_data.append('')
		virustotal_data.append('virustotal')
		virustotal_data.append(domain)
		virustotal_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		virustotal_data_all.append(virustotal_data)
	return virustotal_data_all
def extend_fullhunt(data,domain):
	fullhunt_data_all=[]
	domains=data['hosts']
	for i in domains:
		fullhunt_data=[]
		fullhunt_data.append(i)
		fullhunt_data.append('')
		fullhunt_data.append('')
		fullhunt_data.append('fullhunt')
		fullhunt_data.append(domain)
		fullhunt_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		fullhunt_data_all.append(fullhunt_data)
	return fullhunt_data_all

def extend_crt_sh(data,domain):
	crt_data_all=[]
	for i in data:
		#print (i)
		if "\n" in i['name_value']:
			i_s=i['name_value'].split('\n')
			for j in i_s:
				crt_data=[]
				if "*." in j:
					j=j.replace("*.","")
				crt_data.append(j)
				crt_data.append("")
				crt_data.append("")
				crt_data.append("crt.sh")
				crt_data.append(domain)
				crt_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
				crt_data_all.append(crt_data)
		else:
			crt_data=[]
			j2=i['name_value']
			if "*." in j2:
				j2=j2.replace("*.","")
			crt_data.append(j2)
			crt_data.append("")
			crt_data.append("")
			crt_data.append("crt.sh")
			crt_data.append(domain)
			crt_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
			crt_data_all.append(crt_data)
	return crt_data_all

def extend_zoomeye(data,domain):
	zoomeye_data_all=[]
	for i in data:
		zoomeye_data=[]
		if str(i['name']).endswith('.cjia.com'):
			zoomeye_data.append(str(i['name']))
			zoomeye_data.append(str(i['ip']))
			zoomeye_data.append('')
			zoomeye_data.append('zoomeye')
			zoomeye_data.append(domain)
			zoomeye_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
			zoomeye_data_all.append(zoomeye_data)
	return zoomeye_data_all

def extend_rapiddns(data,domain):
	rapiddns_data_all=[]
	for i in data:
		rapiddns_data=[]
		rapiddns_data.append(i)
		rapiddns_data.append("")
		rapiddns_data.append("")
		rapiddns_data.append("rapiddns")
		rapiddns_data.append(domain)
		rapiddns_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		rapiddns_data_all.append(rapiddns_data)
	return rapiddns_data_all

def extend_chaziyu(data,domain):
	chaziyu_data_all=[]
	for i in data:
		chaziyu_data=[]
		chaziyu_data.append(i)
		chaziyu_data.append("")
		chaziyu_data.append("")
		chaziyu_data.append("chaziyu")
		chaziyu_data.append(domain)
		chaziyu_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		chaziyu_data_all.append(chaziyu_data)
	return chaziyu_data_all

def extend_dnsscan(data,domain):
	dnsscan_data_all=[]
	for i in data:
		dnsscan_data=[]
		dnsscan_data.append(i)
		dnsscan_data.append("")
		dnsscan_data.append("")
		dnsscan_data.append("dnsscan")
		dnsscan_data.append(domain)
		dnsscan_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		dnsscan_data_all.append(dnsscan_data)
	return dnsscan_data_all

def extend_certspotter(data,domain):
	certspotter_data_all=[]
	for i in data:
		certspotter_data=[]
		certspotter_data.append(i)
		certspotter_data.append("")
		certspotter_data.append("")
		certspotter_data.append("certspotter")
		certspotter_data.append(domain)
		certspotter_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		certspotter_data_all.append(certspotter_data)
	return certspotter_data_all

def extend_threatminer(data,domain):
	threatminer_data_all=[]
	for i in data:
		threatminer_data=[]
		threatminer_data.append(i)
		threatminer_data.append("")
		threatminer_data.append("")
		threatminer_data.append("threatminer")
		threatminer_data.append(domain)
		threatminer_data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
		threatminer_data_all.append(threatminer_data)
	return threatminer_data_all


def save_excel(data,path):
	temp_liebiao=[]
	wb=openpyxl.Workbook()
	ws=wb.active
	ws.cell(1,1).value='子域名'

	ws.cell(1,2).value='子域名存活'
	ws.cell(1,3).value='http或https'
	ws.cell(1,4).value='状态码'
	ws.cell(1,5).value='返回长度'

	ws.cell(1,6).value='IP'
	ws.cell(1,7).value='端口'
	ws.cell(1,8).value='数据来源'
	ws.cell(1,9).value='搜索字段'
	ws.cell(1,10).value='搜索时间'
	j=2
	length_data=len(data)
	yiban=length_data/2
	yiban=math.ceil(yiban)
	sifenzhiyi=length_data/4
	sifenzhiyi=math.ceil(sifenzhiyi)
	s=0
	for i in data:
		if s==sifenzhiyi:
			logger.log('INFOR',"已完成25%子域名存活探测，当前域名：{}，请耐心等候...".format(i[0]))
		if s==yiban:
			logger.log('INFOR',"已完成50%子域名存活探测，当前域名：{}，请耐心等候...".format(i[0]))
		s=s+1
		if i[0] not in temp_liebiao:
			temp_liebiao.append(i[0])
			ws.cell(j,1).value=str(i[0])
			cs1,cs2,cs3,cs4=check_alive(i[0])
			#检测网页。
			ws.cell(j,2).value=str(cs1)
			ws.cell(j,3).value=str(cs2)
			ws.cell(j,4).value=str(cs3)
			ws.cell(j,5).value=str(cs4)

			ws.cell(j,6).value=str(i[1])
			ws.cell(j,7).value=str(i[2])
			ws.cell(j,8).value=str(i[3])
			ws.cell(j,9).value=str(i[4])
			ws.cell(j,10).value=str(i[5])
			j=j+1
		domain=str(i[4])
	logger.log('INFOR',"去重后获取到{}子域名的数量为{}。".format(domain,len(temp_liebiao)))
	wb.save(path)
	#print (temp_liebiao)

