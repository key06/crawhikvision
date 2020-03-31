#!/usr/bin/python3
#-*-coding:utf-8-*-
#@Time:2020/3/31 10:30
#@Author:keyshinary
#@File:海康人脸识别产品爬虫.py
#@Software:PyCharm
import requests
from bs4 import BeautifulSoup
import random
import requests
import re
import time

#解析网页
def get_content(url):
    agents = [
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
        "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
        "Mozilla/3.01Gold (Win95; I)",
        "Mozilla/4.8 [en] (Windows NT 5.1; U)",
        "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    ]
    header = {
        'Referer': url,
        'Sec-Fetch-Mode': 'no-cors'}
    agent = random.choice(agents)
    header["User_Agent"] = agent
    response = requests.get(url, headers=header)
    content = response.text.encode('ISO-8859-1').decode('utf-8')  # 解码
    return content


#获取产品列表
def get_product_list(product_url):
    content=get_content(product_url)
    regex='a href=\'(prgs.*?.html)'
    pat=re.compile(regex)
    product_old_list=pat.findall(content)#匹配产品列表
    product_new_list=['https://www.hikvision.com/cn/'+i for i in product_old_list]
    return product_new_list



#解析详情页参数
def get_detail(datalist):
    for each in datalist:
        content=get_content(each)
        content=BeautifulSoup(content,'lxml')
        name=content.find_all(name='div',attrs={'class':'prdo5'})[0].text
        content=content.find_all(id='message')
        content = content[0].find_all('span')
        for each in content:
            if each=='':
                pass
            else:
                with open("{}.txt".format(name[:10]),'a',encoding='utf-8') as f:#保存路径为当前目录
                    f.write(each.text+'\n')
        print(name + "正在录入...")
        time.sleep(1)#睡一秒，防止请求频繁

product_url='https://www.hikvision.com/cn/prlb_1608.html'# 取类别 AI类为1608,1609,1610,1611,1612,1695,1656,1701,1710



list_data=get_product_list(product_url)
list_data=list(set(list_data))
get_detail(list_data)