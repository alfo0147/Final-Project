# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 19:05:25 2017

@author: User
"""


import pandas as pd
import json
import os
import re
import numpy as np
from bs4 import BeautifulSoup
import requests
from pandas import Series, DataFrame
import time

MovieData=pd.read_csv(r'C:\dataset.csv', encoding='CP949')
date=pd.read_csv(r"C:\opendate2.csv", encoding='cp949')

Movies=[i for i in MovieData['영화명']]
Director=[i for i in MovieData['감독']]

#영화와 함께 감독명을 검색하기 위하여 영화 감독 검색 리스트를 만들기
Search=zip(Director,Movies)


Plus=[]
for i in Search:
    a=list(i)
    Plus.append(a)
    

MovieDirector=[]
for i in Plus:
    b=' '.join(i)
    MovieDirector.append(b)

MovieDirector = DataFrame(MovieDirector)


#검색리스트와 기간을 url에 넣을 수 있는 함수
def URLmaker(query,sdate,edate):
    try:
        base_url = 'http://news.naver.com/main/search/search.nhn?query={}&startDate={}&endDate={}'
        encoded_query=requests.utils.quote(query, encoding='MS949')     
        base_url = base_url.format(encoded_query, sdate, edate)
    except:
        print(i)
        pass
    return base_url

#앞에 만든 함수에 검색과 기간을 넣어서 최종 url 생성
FinalUrl=[]
for i in range(len(MovieDirector)):
    url=URLmaker(MovieDirector[0][i], date['sdate'][i], date['edate'][i])
    FinalUrl.append(url)

#각 url 페이지에서 기사수 가져오기
countlist=[]
for n,i in enumerate(FinalUrl):
    try:
        r = requests.get(i).text
        soup = BeautifulSoup(r,'html.parser')
        cnt = soup.find('span', class_='result_num').text
        cnt = cnt.replace(',','')
        cnt2 = re.findall('[0-9]+',cnt)
        print(n)
    except:
        print(n,i)
        pass
    countlist.append((Movies[n],cnt2[2]))
    time.sleep(1)  

#튜플에 있는 기사수 리스트 안에 넣기
Clist=[]
for i in countlist:
    b=list(i)
    Clist.append(b)

#기사수에 영화명 넣어서 데이터 프레임 만들기
CL=DataFrame(Clist,Columns=['영화명', 'count'])
CL.columns = [['영화명','count']]
CL.head(2)

#기사수와 데이터 프레임에 합치기
merge = DataFrame.merge(MovieData,CL,on='영화명')
merge.head(3)

#데이터 프레임 저장
merge.to_csv('dataset_count.csv')