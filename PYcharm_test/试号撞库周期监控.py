# _*_ coding: utf-8 _*_

import psycopg2 as pg
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
import xlwt, xlrd
from xlutils.copy import copy
import time
import StringIO

# output = StringIO.StringIO()
# output.write('abc.\n')
# print >>output, 'def.'
# print(output)
# contents = output.getvalue()
# output.close()


db = 'credit'
user = 'dev'
host = '192.168.91.11'
port = '5433'
password = '123456'

# 小贷APP
sql1 = '''
--特殊设备ID对应custid|number数，及其出现时间
select 
a.deviceid,min(logintime) as 首次出现时间,
max(logintime) as 最近一次出现时间,
count(distinct a.custid) as 尝试登录失败的custid数,
count(distinct a.telno) as 尝试登录失败的手机号数,
count(a.logintime) as 尝试登录次数,
count(distinct a.logindate) as 共尝试登录天数

from credit.custloginfaillog a
where a.deviceid in (
select distinct a.deviceid from(
select 
a.logindate,a.deviceid,count(distinct a.telno) as loginfailcustcnt
from (
select 
--某号某天某设备失败次数
a.telno, a.logindate, a.deviceid, count( logintime ) as loginfailcnt
from credit.custloginfaillog a
where a.ip != '211.152.59.204' and a.ip != '211.152.59.203'
group by 1,2,3
) a
where a.logindate::timestamp >= current_date - interval '90 day'
group by 1,2
having count(distinct a.telno) > 500
)  as a )
group by 1
order by 1
;

'''

# 米多多APP
sql2 = '''
--特殊设备ID对应custid|number数，及其出现时间
select 
a.deviceid,min(logintime) as 首次出现时间,
max(logintime) as 最近一次出现时间,
count(distinct a.custid) as 尝试登录失败的custid数,
count(distinct a.telno) as 尝试登录失败的手机号数,
count(a.logintime) as 尝试登录次数,
count(distinct a.logindate) as 共尝试登录天数

from jumi.custloginfaillog a
where a.deviceid in (
select distinct a.deviceid from(
select 
a.logindate,a.deviceid,count(distinct a.telno) as loginfailcustcnt
from (
select 
--某号某天某设备失败次数
a.telno,a.logindate,a.deviceid,count(logintime) as loginfailcnt
from jumi.custloginfaillog a
-- where a.ip != '211.152.59.204' and a.ip != '211.152.59.203'
group by 1,2,3
) a
where a.logindate::timestamp >= current_date - interval '90 day'
group by 1,2
having count(distinct a.telno) > 5
)  as a )
group by 1
order by 1
;
'''

# 米多多_设备VS微信
sql3 = '''
SELECT 
       deviceid,count(distinct wxopenid) as cnt_wxopenid,count(distinct ip) as cnt_ip,
       max( logindate) as max_logindate, min(logindate) as min_logindate
  FROM jumi.custloginfaillog group by 1
  order by 2 desc;
'''

# 米多多_IP VS 微信
sql4 = '''
SELECT 
       ip,count(distinct wxopenid) as cnt_wxopenid,count(distinct deviceid) as cnt_deviceid,
       max( logindate) as max_logindate, min(logindate) as min_logindate
  FROM jumi.custloginfaillog group by 1
  order by 2 desc;
'''
sql5 = '''
SELECT 1+1;
'''

conn = pg.connect(database = db, user = user, password = password, host = host, port = port)
cur = conn.cursor()
cur.execute(sql1)
result_sql1 = cur.fetchall()
# cur.execute(sql2)
# result_sql2 = cur.fetchall()
# result_sql2_col = cur.description
cur.close()
conn.close()


str_result_sql1 = StringIO.StringIO()
for i in range(len(result_sql1)):
    str_result_sql1.write(result_sql1[i])
    str_result_sql1.write('\n')
email_text = str_result_sql1.getvalue()
str_result_sql1.close()
print(email_text)
print(type(email_text))
# 发邮件
sender = 'chenzhiwei@zealfi.com'
password = 'ZEALFIczw1CZW'

receivers = ['chenzhiwei@zealfi.com']
sentto = ['chenzhiwei@zealfi.com']
acc = ['chenzhiwei@zealfi.com']

COMMSPACE = ','
msg = MIMEMultipart()
msg['from'] = sender
msg['To'] = COMMSPACE.join(sentto)
msg['Cc'] = COMMSPACE.join(acc)
msg['Subject'] = Header(u'试号撞库周期监控' + time.strftime('%Y-%m-%d',time.localtime(time.time())))
print result_sql1
print type(result_sql1)
msg.attach(MIMEText(email_text, 'plain'))
# try:
#     smtpObj = smtplib.SMTP(timeout=10000000)
#     smtpObj.connect('mail.zealfi.com')
#     smtpObj.login(sender, password)
#     smtpObj.sendmail(sender, receivers, msg.as_string())
#     smtpObj.quit()
#     print "sent success"
# except smtplib.SMTPException:
#     print "sent email fail"

try:
    smtpObj = smtplib.SMTP(timeout=10000000)
    smtpObj.connect('mail.zealfi.com')
    smtpObj.login(sender, password)
    smtpObj.sendmail(sender, receivers, msg.as_string())
    print "sent success"
except smtplib.SMTPException as e:
    print "sent email fail"
    raise e
finally:
    smtpObj.quit()



# smtpObj = smtplib.SMTP(timeout=10000000)
# smtpObj.connect('mail.zealfi.com')
# smtpObj.login(sender, password)
# smtpObj.sendmail(sender, receivers, msg.as_string())
# smtpObj.quit()
# print "sent success"