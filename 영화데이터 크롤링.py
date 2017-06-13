# -*- coding: utf-8 -*-
"""
Created on Fri May 26 09:25:22 2017

@author: KEJ
"""

# 영화진흥원 데이터 크롤링
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup as bsoup
import codecs
import re
import os

# 웹 드라이버를 이용
driver = webdriver.Chrome(r'C:\Users\KEJ\chromedriver_win32\chromedriver.exe')
driver.implicitly_wait(2)


# 크롤링 데이터 기간 설정
import datetime
import time

def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    time_delta = abs((d2 - d1).days)
    

    daylist = []
    for i in range(time_delta+1):
        nd = datetime.datetime.strptime(sdate, "%Y-%m-%d") + datetime.timedelta(i)
        daylist.append(nd.strftime('%Y-%m-%d'))
    return daylist

sdate = '2012-01-01'
edate ='2017-04-20'
day_list = days_between(sdate, edate)


# 데이터 수집과 파일 이름 정의
import os
import datetime

now = datetime.datetime.now().strftime('%Y-%m-%d')

for i in day_list:
    driver.get(r'http://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do?loadEnd=0&searchType=search&sSearchFrom='+str(i)+'&sSearchTo='+str(i))
    
    driver.find_element_by_class_name('btn_type01').click() # 예/아니오 창

    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to_alert().accept()
    except TimeoutException:
        print("Alert not found. Move on...")
        
    time.sleep(4) 
    os.rename(r'C:\Users\KEJ\Downloads\일별박스오피스_' + now  +'.xls',
              'box_'+str(i)+'.xls')
    # 데이터 타입이 html파일

