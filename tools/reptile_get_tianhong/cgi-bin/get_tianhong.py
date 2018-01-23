#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2,re,time
from module.fundDB import fund_tab
from module.get_access_ip import getip
gip=getip()
access_ip=gip.ipinfo()
response = urllib2.urlopen("http://www.howbuy.com/fund/ajax/gmfund/valuation/valuationnav.htm?jjdm=000961")
content= response.read()
#print content
latestValue = re.findall(r'con_value con_value_up\">(.*)</',content)[0]
latestPercent= re.findall(r'con_ratio_red\">(.*)</',content)[0]

Nowtime=time.strftime('%Y-%m-%d %H:%M:%S')
#print(latestValue)
#print(latestPercent)
earnings = float(latestValue)*63351.09-79930.07


class usedb():
    f = fund_tab()
    def insert_db(self):
        self.f.value=latestValue
        self.f.percent=latestPercent
        self.f.date=time.strftime('%Y-%m-%d %H:%M:%S')
        self.f.save()
    def query_db(self):
        t_list=self.f.select().order_by(fund_tab.date.desc()).limit(1)
        for T in t_list:
            global last_value,last_date,last_percent
            last_value=T.value
            last_date=T.date
            last_percent=T.percent

db=usedb()
db.query_db()
db.insert_db()
print(last_value)
html = """

<html>
    <head>
        <meta charset="UTF-8">
        <title>
        Alvin 天弘基金收益
        </title>
    </head>
    <body>
        <p>
        当前IP地址：%s
        上次天弘天弘沪深300指数估值：%s ， 涨幅是 %s 查询时间是 %s </br>
        最新天弘天弘沪深300指数估值：%s ， 涨幅是 %s 当前时间是 %s
        </p>
        <p>
           我的天弘基金收益：￥ %s
        </p>
        <p>
            Alvin Wan  
        </p>
    </body>
</html>

"""
print("Content-type:text/html")
print()
print(html%(access_ip,last_value,last_percent,last_date,latestValue,latestPercent,Nowtime,earnings))