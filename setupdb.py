# -*- coding: UTF-8 -*-

import pymysql

db_host = ""
db_user = ""
db_passwd = ""
db_name = ""

db_host = input("HOST:")
db_user = input("USER NAME:")
db_passwd = input("Password:")
db_name = input("DATABASE NAME:")

db = pymysql.connect(db_host,db_user,db_passwd,db_name)
cur = db.cursor()

sql = """CREATE TABLE qqinfo(
		 userqq CHAR(15), 
		 qq CHAR(15),
		 nick TEXT,
		 sex TEXT,
		 age INT,
		 birthday TEXT,
		 constellation TEXT,
		 occupation TEXT,
		 company TEXT,
		 college TEXT,
		 location TEXT,
		 hometown TEXT,
		 email CHAR(50),
		 friendship_day INT)default charset = utf8"""

cur.execute(sql)
db.close()

print("DONE")