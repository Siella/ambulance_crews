import requests
import pandas as pd
import re
import json
from bs4 import BeautifulSoup
#https://kazan.nuipogoda.ru/1-%D0%B4%D0%B5%D0%BA%D0%B0%D0%B1%D1%80%D1%8F#2019
year=[['январь',31], ['февраль',29 ],['март' ,31], ['апрель',30], ['май',31],[ 'июнь',30], ['июль',31], ['август',31], ['сентябрь',30], ['октябрь',31], ['ноябрь',30],[ 'декабрь',31]]
url ='https://kazan.nuipogoda.ru/1-января#2019'
years=['2019','2020']

def parse(teg, cls,soup):
    time = soup.find_all(teg, class_=cls)
    times = []
    for one in time:
        times.append(one.next)
    return times
def evday(url,day,month,year):
    if month=="январь" and day==1 and year==2019:
        pass
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        weather=parse('div','cl_title',soup)[18:27]
        time=parse("span","c1",soup)[18:27]
        temp=parse('span','ht',soup)[18:27]
        w_spid=parse('span','ws',soup)[18:27]
        p=parse('span','p',soup)[18:27]
        df = pd.DataFrame({'dr':day+month+year,'time': time, 'weather': weather,'temp':temp,'w_spid': w_spid,'p':p})
    return df

df=evday(url,'1','января','2019')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
weather=parse('div','cl_title',soup)[18:27]
time=parse("span","c1",soup)[18:27]
temp=parse('span','ht',soup)[18:27]
w_spid=parse('span','ws',soup)[18:27]
p=parse('span','p',soup)[18:27]
df = pd.DataFrame({'dr':'1 декабря 2019','time': time, 'weather': weather,'temp':temp,'w_spid': w_spid,'p':p})
for yr in years:
    for i in  year:
        for j in range (i[1]):
            day=str(j)
            url=f'https://kazan.nuipogoda.ru/{j}-{i[0]}#{yr}'
            df_new=evday(url,day,i[0],yr)
            df=pd.concat((df_new, df))
    #url=f'https://kazan.nuipogoda.ru/{j}-{i[0]}#2019'
df.to_csv ('weather.csv', index = False, header=True)



