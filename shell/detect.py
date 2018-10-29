#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 
import sys
import os
import base64
import constans
import json
import socket
import struct
import time
import log
from subprocess import Popen, PIPE
import threading
# from multiprocessing import Pool, Manager
import is_connect
import process
import traceback
import Queue

# manager = Manager()
# prl = manager.list()
result_queue = Queue.Queue()


def setConfig():
    configPath = '/tmp/conf/busi.conf'
    # if os.path.isfile(configPath) == False:
    #     writeFile = open(constans.APP + "/1", "w")
    #     err = 'Cannot open file : ' + configPath
    #     writeFile.write(err)
    #     print(err)
    #     writeFile.close()
    #     return 'err'
    print time.ctime() + '-Reading conf...-'
    config = open(configPath)
    baseLine = config.read()
    configStr = base64.decodestring(baseLine)
    local = configStr.find('\n')
    tmpdata = configStr[:local]  # first line is IP infomation
    tmpdata = tmpdata.replace('\r', '')
    jdata = eval(tmpdata)
    result = (str(jdata["task_id"]), str(jdata["task_name"]), str(jdata["vul_id"]), jdata["dst_ip"])
    content = configStr[local + 1:]  # the rest of configStr is python scripts
    # print content
    shellFile = open("/iie_test.py", "w")
    shellFile.write(content)
    shellFile.close()
    return result


def doShExec(task_id, task_name, vul_id, ip):
    log.task_run()
    os.system('chmod 777 /iie_test.py')
    argv = ['python /iie_test.py ' + ip]
    print time.ctime() + '-' + ip + '-Executing shell-'
    p = Popen(argv, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    mtime = time.strftime('%Y-%m-%d %H:%M:%S')
    if stderr:
        print(stderr)
        data = mtime + ';Err;' + task_id + ';' + vul_id + ';' + task_name + ';' + ip + ';Err;Err\n'
        result_queue.put(data)
        log.task_run_fail()
        log.write_error_to_appstatus(str('script error: ' + stderr), -1)
    print time.ctime() + '-' + ip + '-Finished-'
    rlist = stdout.split('\n')
    tmpresultlist = rlist[-2].split(';')
    try:
        data = mtime + ';' + tmpresultlist[0] + ';' + task_id + ';' + vul_id + ';' + task_name + ';' + ip + ';' + tmpresultlist[1] + ';' + tmpresultlist[2]  + '\n'
        result_queue.put(data)
        log.task_run_success()
    except Exception as e:
        print(e)
        #data = mtime + ';Err;' + task_id + ';' + vul_id + ';' + task_name + ';' + ip + '\n'
        #result_queue.put(data)
        #log.task_run_fail()
        #log.write_error_to_appstatus(str(e), -1)
    return data


def writeResult():
    log.write_result()
    try:
        writeFile = open(constans.RLT + "/sh_001.result", "w")
        while not result_queue.empty():
            writeFile.write(result_queue.get())
        writeFile.close()
        print time.ctime() + '-Writing Result File Finished-'
        log.write_result_success()
    except Exception as result_e:
        print(result_e)
        print('write err')
        log.write_result_fail()
        log.write_error_to_appstatus(result_e, -1)


if __name__ == '__main__':
    log.task_start()
    if not os.path.exists(constans.APP):
        os.makedirs(constans.APP)
    if not os.path.exists(constans.LOG):
        os.makedirs(constans.LOG)
    if not os.path.exists(constans.RLT):
        os.makedirs(constans.RLT)
    ipList = []
    resultList = []
    # pool = Pool(16)
    log.get_conf()
    mid = ()
    # 判断网络
    is_connect.Update()
    try:
        mid = setConfig()
        log.get_conf_success()
    except Exception as conf_e:
        print(conf_e)
        traceback.print_exc()
        log.get_conf_fail()
        log.write_error_to_appstatus(str(conf_e), -1)

    ip_set = mid[3]
    # print len(ip_set)
    if len(ip_set) != 0 and len(ip_set) != 1:
        if ip_set.find(',') != -1:
            ipList = ip_set.split(',')
        elif ip_set.find('-') != -1:
            ipStr = ip_set.split('-')
            ipInt1 = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ipStr[0])))[0])
            ipInt2 = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ipStr[1])))[0])
            for i in xrange(ipInt1, ipInt2 + 1):
                ipList.append(socket.inet_ntoa(struct.pack('I', socket.htonl(i))))
        else:
            ipList.append(ip_set)
        try:
            threads = []
            for i in ipList:
                t = threading.Thread(target=doShExec, args=(mid[0], mid[1], mid[2], i))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
                #pool.apply_async(doShExec, (mid[0], mid[1], mid[2], i))
            # resultList.append(tmp)
            #pool.close()
            # pool.join()
            writeResult()
            writeFile = open(constans.APP + "/0", "w")
            writeFile.close()
            log.task_success()
        except Exception as e:
            writeFile = open(constans.APP + "/1", "w")
            writeFile.write('Exec the upload python script occurs error')
            writeFile.close()
            log.task_fail()
            log.write_error_to_appstatus(str(e), -1)
    else:
        try:
            tmp = doShExec(mid[0], mid[1], mid[2], 'http')
            result_queue.put(tmp)
            writeResult()
            writeFile = open(constans.APP + "/0", "w")
            writeFile.close()
            log.task_success()
        except Exception as main_e:
            print(main_e)
            print('main err')
            log.task_fail()
            log.write_error_to_appstatus(main_e, -1)

    # logfile = open(constans.LOG+'/'+addressSegment[0]+'.log','w')
    # logfile.write(addressSegment[0])
    # logfile.close()
