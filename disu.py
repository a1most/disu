from modules.log import *
from modules.module import *

import os
from optparse import OptionParser
from multiprocessing import Pool
from functools import partial

domains=[]
def data_fenxi(folder):
	for i in os.listdir(folder):
		with open(folder+'//'+i,'r') as f:
			data=f.readlines()
			for j in data:
				if not j.strip() in domains and j.strip()!="":
					domains.append(j.strip())
	#此函数整理从文件中获取到的domain信息。
				
if __name__=='__main__':
	global folder,single_domain,output
	usage = """usage: 
	%prog -f C:\\Users\\Administrator\\Desktop
	%prog -d baidu.com -o C:\\Users\\Administrator\\Desktop\\1.txt"""
	parser = OptionParser(usage)

	parser.add_option("-f", "--folder", dest="folder",type='string',default=None,help="Who is the target group?")
	parser.add_option("-d", "--domain", dest="single_domain",type='string',help="who is the target?")
	#parser.add_option("-o", "--output", dest="output",type='string',default=None,help="where is the output?")
	options, args = parser.parse_args()
	
	folder,single_domain=options.folder,options.single_domain
	#以上为从参数获取数据。


	#以上代码
	if folder:
		data_fenxi(folder)
		for jjj in domains:
			getdata(jjj)
		print (domains)
		#进程传入列表，会对列表中的值自动进行解析。
	elif single_domain:
		if '.' in single_domain:
			getdata(single_domain,single='1')
		else:
			print ("请输入一个正确的域名信息： baidu.com")
	else:
		print ("请输入域名相关信息:-f/-d")
	#逻辑为：是否从文件获取域名，有则判断是否输入线程信息;无则判断是否直接获取域名，是则判断是否正确的域名。
