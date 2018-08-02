# -*- coding: UTF-8 -*- 

import selenium
from selenium import webdriver
import time
import re
import random
import pymysql
import sys

myqq = ""
passwd = ""
dir = "qq.vcf"
db_host = ""
db_user = ""
db_passwd = ""
db_name = ""

#browser = webdriver.Chrome()

def login():
	global myqq,passwd,db_host,db_user,db_passwd,db_name,dir
	browser.get("https://user.qzone.qq.com/")
	browser.switch_to_frame('login_frame')
	log = browser.find_element_by_id("switcher_plogin")
	log.click()
	time.sleep(1)
	username = browser.find_element_by_id('u')
	username.send_keys(myqq)
	ps = browser.find_element_by_id('p')
	ps.send_keys(passwd)
	btn = browser.find_element_by_id('login_button')
	time.sleep(2)
	btn.click()
	time.sleep(2.5)
	return

def get_date(friend_qq):
	global myqq,passwd,db_host,db_user,db_passwd,db_name,dir
	try:
		url = "https://user.qzone.qq.com/" + myqq + "/friendship?fuin=" + friend_qq
		#print(url)
		browser.get(url)
		browser.implicitly_wait(5)
		browser.switch_to_frame("app_canvas_frame")
		str1 = browser.find_element_by_id("id_friendshipdays").get_attribute('innerHTML')
		#print(str1)
		res = re.findall("[0-9]+",str1)
		day = ''
		for x in res:
			day = day + x
		print("friend date:"+day)
		sql = 'UPDATE qqinfo SET friendship_day = "'+str(day)+'"WHERE qq = "'+str(friend_qq)+'"'
		cur.execute(sql)
	finally:
		return day
		

def get_info(friend_qq):
	global myqq,passwd,db_host,db_user,db_passwd,db_name,dir
	try:
		url = "http://ti.qq.com/qcard/index.html?qq=" + friend_qq
		#print(url)
		browser.get(url)
		time.sleep(2)
		browser.implicitly_wait(3)
		
		#nick name:
		nick = browser.find_element_by_id("nick").text
		print("nick:"+nick)
		
		#sex:
		sex = browser.find_element_by_id("gender").text
		print("sex:"+sex)
		
		#age:
		age = browser.find_element_by_id("age").text
		print("age:"+age)
		
		#birthday
		birthday = browser.find_element_by_id("birthday").text
		print("birthday:"+birthday)
		
		#constellation
		constellation = browser.find_element_by_id("constellation").text
		print("constellation:"+constellation)
		
		#occupation
		occupation = browser.find_element_by_id("occupation").text
		#occupationOBJ = re.search("(?<=\s)\S*$",occupation,flags=0)
		print("occupation:"+occupation)
		#print("occupation:"+occupationOBJ.group(0))
		
		#company
		company = browser.find_element_by_id("company").text
		print("company:"+company)
		
		#college
		college = browser.find_element_by_id("college").text
		print("college:"+college)
		
		#location
		location = browser.find_element_by_id("location").text
		print("location:"+location)
		
		#hometown
		hometown = browser.find_element_by_id("hometown").text
		print("hometown:"+hometown)
		
		#email
		email = browser.find_element_by_id("email").text
		print("email:"+email)
		sql = 'UPDATE qqinfo SET nick = "'+str(nick)+'", sex = "'+str(sex)+'", age = "'+str(age)+'", birthday = "'+str(birthday)+'", constellation = "'+str(constellation)+'", occupation = "'+str(occupation)+'", company = "'+str(company)+'", college = "'+str(college)+'", location = "'+str(location)+'", hometown = "'+str(hometown)+'", email = "'+str(email)+'" WHERE qq = "'+str(friend_qq)+'"'
		cur.execute(sql)
	except:
		print("Unexpected error:", sys.exc_info()[0])
	finally:
		return nick;

		
def get_friends():	#return a list of qq number
	global myqq,passwd,db_host,db_user,db_passwd,db_name,dir
	f = open(dir,"r",encoding = 'utf-8')
	return re.findall("(?<=EMAIL:)[0-9]+",f.read())


def main():
	global myqq,passwd,db_host,db_user,db_passwd,db_name,dir
	
	friends = get_friends()
	
	login()
	i = 0;
	for qq in friends:
		print("==============================")
		print("Collect:"+qq)
		
		sql = 'INSERT INTO qqinfo (userqq,qq) VALUE ("'+myqq+'","'+qq+'")'
		cur.execute(sql)
		db.commit()
		
		time.sleep(2+random.random()*5)
		while get_info(qq) == '':
			print("RELOAD , SLEEP = 60")
			db.rollback()
			time.sleep(60)
		db.commit()
		
		time.sleep(2+random.random()*5)
		while get_date(qq) == '':
			print("RELOAD , SLEEP = 5")
			db.rollback()
			time.sleep(5)
		db.commit()
		
		i=i+1
		if i%4==0:
			b = 10+random.random()*10
			if i%8==0:
				#b = b + 60
				b = b
			print("=============================================Sleep:"+str(b))
			time.sleep(b)
		
			
	
	browser.close()
	db.commit()
	db.close()
	print("+++++complite+++++")
	return

	
#START	
	
print("QQ friend info collecter(test version by hanson)")
print("Please read readme file before use this program!")
print("login info:")
myqq = input("QQ number:")
passwd = input("QQ Password:")
db_host = input("HOST:")
db_user = input("USER NAME:")
db_passwd = input("Password:")
db_name = input("DATABASE NAME:")
browser = webdriver.Chrome()

db = pymysql.connect(db_host,db_user,db_passwd,db_name)
cur = db.cursor()	
main()
