

######### read html to csv in working directory file
import pandas as pd
from bs4 import BeautifulSoup as bsoup
import codecs
import re
import os

# html 영화 데이터가 저장되어있는 파일에서 데이터를 불러옴
input_dir = r'C:\Users\KEJ\box_movie'
file_list = []

for root, dirs, files in os.walk(input_dir):
    for file in files:
        fileName = input_dir+'/'+file
        input_file = codecs.open(fileName, 'r',encoding='utf-8')
        
        soup= bsoup(input_file.read())
        file_list.append(soup)
        
        input_file.close()

# col_header
col_header=[]
for c in soup.find_all('th'):
    re_text = c.text
    re_text = re.sub('\n{1}','',re_text)
    re_text = re.sub('\t{1}','',re_text)
    re_text = re.sub('\r{1}','',re_text)
    col_header.append(re_text)
    
##############################
from pandas import DataFrame as df
# col list
dic_day = {}

for idx,soup in enumerate(file_list):
    tr_list = soup.find_all("tr")
    
    df_li = []
    for i in range(1, len(tr_list)-1):
        col_list = [ele.text for ele in tr_list[i].find_all('td')]
        td_list =[]
        for c in col_list:   
            re_text = c
            re_text = re.sub('\n{1}','',re_text)
            re_text = re.sub('\t{1}','',re_text)
            re_text = re.sub('\r{1}','',re_text)
            td_list.append(re_text)
        df_li.append(td_list)        
    
    soup.findAll('div','board_tit')
    date = soup.find_all('h4')[0].text
    
    movie_day = df(df_li,columns = col_header)
    movie_day['date'] = date
    dic_day.append(movie_day,ignore_index=True)
    
    dic_day[idx] = df(df_li,columns = col_header)
    dic_day[idx]['date'] = date

    
# total data_frame 
colName = ['date']+col_header
df_total = df(columns=colName)
for k in dic_day.keys():
    df_total = df_total.append(dic_day[k],ignore_index=True)
    
df_total = df_total[colName]

# export csv file  
df_total.to_csv("total_movie.csv",index=False,encoding='utf-8')          
            
