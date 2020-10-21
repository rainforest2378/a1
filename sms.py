# -*- coding: utf-8 -*-
'''
#intent      :
#Author      :Michael Jack hu
#start date  : 2019/1/13
#File        : msg.py
#Software    : PyCharm
#finish date :
'''

import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import pymysql
import datetime
import json
import schedule

def check():
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    return_dict = []
    # 执行sql语句
    startTime = datetime.datetime.now()

    print(startTime)
    endtime = startTime - datetime.timedelta(days=1)
    print(endtime)
    # while datetime.datetime.now() < startTime:
    # with conn.cursor() as cursor:

    # 9.select * from 表 where datediff(day,scantime,getdate())=1
    sql = "select hostip,scantime from os_detection  where datediff(scantime,now())=-1 order by inet_aton(hostip)"

    cursor.execute(sql)
    result = cursor.fetchall()
    arry1 = []
    arry2 = []
    for it in result:

        res = {}

        hip = it[0]

        stime = it[1]

        # str = '{}-{}-{}'.format(stime.year, stime.month, stime.day)
        # startTime = datetime.datetime.strptime(str, '%Y-%m-%d')
        # print(startTime)
        if stime.hour == 1:
            # print(hip,stime)
            arry1.append(hip)

    print(arry1)

    sql2 = "select hostip,scantime from os_detection  where datediff(scantime,now())=0 order by inet_aton(hostip)"

    cursor.execute(sql2)
    result2 = cursor.fetchall()
    for it in result2:
        res = {}
        hip = it[0]
        stime = it[1]

        # str = '{}-{}-{}'.format(stime.year, stime.month, stime.day)
        # startTime = datetime.datetime.strptime(str, '%Y-%m-%d')
        # print(startTime)
        if stime.hour == 1:
            # print(hip,stime)
            arry2.append(hip)

    print(arry2)

    iparr1 = []
    for i in range(len(arry1)):
        x = arry1[i].split(".", -1)
        iparr1.append(x[-1])
    print(iparr1)

    iparr2 = []
    for i in range(len(arry2)):
        x = arry2[i].split(".", -1)
        iparr2.append(x[-1])
    print(iparr2)
    # print((arry1[10:len(arry1) - 1]))

    ii = 0
    jj = 0
    resa = []
    resb = []

    while (1):
        if ii == len(iparr1) and jj == len(iparr2):
            break
        if ii == len(iparr1):
            print(iparr2[jj:len(iparr2)])
            resb.extend(iparr2[jj:len(iparr2)])
            break
        if jj == len(iparr2):
            print(iparr1[ii:len(iparr1)])
            resa.extend(iparr1[ii:len(iparr1)])
            break

        if (iparr1[ii] == iparr2[jj]):
            ii += 1
            jj += 1
        elif (iparr1[ii] < iparr2[jj]):
            resa.append(iparr1[ii])
            ii += 1
        else:
            resb.append(iparr2[jj])
            jj += 1

    print(resa)  # 关了
    print(resb)  # 开了

    str1 = ' '.join(resa)
    str2 = ' '.join(resb)
    return str1,str2


    #str='%d %d %d'% stime.year,stime.month,stime.day




    #print(stime<startTime)



def sent_message(phone_number,str1,str2):
    p = '10.10.103.'

    text = '\n' + '【扫描结果】:' + '\n' + '关闭:' + p + str1 + '\n' + '打开:' + p + str2

    auth_token = 'd1cd7c1d16f7225344c45c5d8321c314'  # 去twilio.com注册账户获取token
    account_sid = 'ACae1924aa2f37ba2ea7a2a11fd9399cef'

    client = Client(account_sid, auth_token)
    try:
        mes = client.messages.create(
        from_='+12244196361',  # 填写在active number处获得的号码
        body=text,
        to=phone_number)
    except TwilioRestException as e:
        print(e)
    print("OK")

s1,s2=check()
#while 1:
#sent_message("+8618810500580",s1,s2)
#time.sleep(3600 * 24)
schedule.every().day.at("07:30").do(sent_message,"+8618810500580",s1,s2) #
schedule.every().day.at("07:31").do(sent_message,"+8613241821896",s1,s2)




while True:
    schedule.run_pending() # 运行所有可运行的任务