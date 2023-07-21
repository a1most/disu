import sqlite3
from modules.log import logger
#存储数据到test.db中。


def savedb_data(data):
	logger.log('INFOR','开始存储数据到数据库中....') 
	conn=sqlite3.connect('test.db')
	cursor=conn.cursor()
	#参考链接https://www.cnblogs.com/lihaiping/p/sqlitedatetime.html
	cursor.execute('''CREATE TABLE IF not exists KONGJIANYINQING ([ID] INTEGER PRIMARY KEY,[域名] VARCHAR(20),[IP] VARCHAR(20),[端口] VARCHAR(20),[数据来源] VARCHAR(20),[搜索字段] VARCHAR(20),[搜索时间] VARCHAR(20),[入库时间] TimeStamp NOT NULL DEFAULT (datetime('now','localtime')));''')
	for i in data:
		#print (i[0],i[1],i[2],i[3],i[4],i[5])
		insert_data='insert or ignore into KONGJIANYINQING([域名],[IP],[端口],[数据来源],[搜索字段],[搜索时间]) values("{}","{}","{}","{}","{}","{}");'.format(str(i[0]),str(i[1]),str(i[2]),str(i[3]),str(i[4]),str(i[5]))
		cursor.execute('''delete from KONGJIANYINQING where KONGJIANYINQING.rowid not in (select MAX(KONGJIANYINQING.rowid) from KONGJIANYINQING group by 域名);''')
		cursor.execute(insert_data)
	"""
	cursor.execute('''insert or ignore into KONGJIANYINQING([域名],[IP],[端口],[数据来源],[搜索字段],[搜索时间]) values('b2b1.baidu.com','127.0.0.1','3305','shodan','baidu.com','2022-07-20');''')
	cursor.execute('''insert or ignore into KONGJIANYINQING([域名],[IP],[端口],[数据来源],[搜索字段],[搜索时间]) values('b2b1.baidu.com','127.0.0.1','3305','shodan','baidu.com','2022-07-20');''')
	cursor.execute('''insert or ignore into KONGJIANYINQING([域名],[IP],[端口],[数据来源],[搜索字段],[搜索时间]) values('b2b.baidu.com','127.0.0.1','3305','shodan','baidu.com','2022-07-21');''')
	cursor.execute('''insert or ignore into KONGJIANYINQING([域名],[IP],[端口],[数据来源],[搜索字段],[搜索时间]) values('b2b.baidu.com','127.0.0.1','3305','shodan','baidu.com','2022-07-21');''')
	cursor.execute('''delete from KONGJIANYINQING where KONGJIANYINQING.rowid not in (select MAX(KONGJIANYINQING.rowid) from KONGJIANYINQING group by 域名);''')
	#此语句根据域名去重。
	"""
	cursor.close()
	conn.commit()
	#logger.log('INFOR',"完成数据存储。")
	conn.close()
