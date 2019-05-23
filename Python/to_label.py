import pandas as pd
import numpy as np

C = ['China',  'France', 'Germany',  'Italy',
       'Japan',  'Poland', 'Russia', 'Spain',
       'Turkey', 'UK', 'USA', 'Vietnam']

source = ['Americans','American',
'American','Arab' ,
'Austrians', 'Bangladeshi','British',
'Czechs' ,'Chinese',
'Chinese','English',
'French' ,'French',
'French','German' ,
'Germans' ,'Greeks' ,
'Hungarians','Italian',
'Italians','Japanese' ,
'Lithuanians' ,'Malays','Poles' ,
'Polish' ,'Portuguese',
'Portugiese','Russian','Russian',
'Russians','Slovakians',
'Spanish','Spanish',
'Turkish','Turks','Vietnamese','Chinese',
'Bangladeshi','China','Hungary','Vietnam','Greece',
'Poland','Malaysia',
'Georgia','UK',
'Japan','Bangladesh',
'USA','Japan',
'Russia','China',
'Kuwait','United Arab Emirates',
'Oman','Saudi Arabia',
'Bahrain','Qatar',
'USA','Russia', 'Austria',
'UK','Malaysia','France',
'USA','sogbesan/Poland','Lithuania',
'Germany','UK','Turkey','CzechRepublic',
'Kuwait','Vietnam','Spain']

dest = ['USA','USA','USA','UnitedArabEmirates','Austria','Bangladesh',
'UK','CzechRepublic','China','China','UK','France','France','France','Germany','Germany',
'Greece','Hungary', 'Italy','Italy','Japan','Lithuania','Malaysia','Poland',
'Poland','Portugal','Portugal','Russia','Russia','Russia', 'Slovakia','Spain','Spain','Turkey',
'Turkey','Vietnam','China','Bangladesh','China','Hungary','Vietnam','Greece','Poland','Malaysia',
'Georgia','UK','Japan','Bagladesh','USA','Japan',
'Russia','China', 'Kuwait','UnitedArabEmirates','Oman','SaudiArabia',
'Bahrain','Qatar','USA','Russia', 'Austria','UK','Malaysia',
'France','USA','Poland','Lithuania','Germany','UK','Turkey',
'CzechRepublic','Kuwait','Vietnam','Spain']   

def _label(df):
    df = df[df['country'].isin(C)]
    lista = []
    for i in list(range(df.shape[0])):
        a = df['label'][i]
        b = a.split('/')[5]    
        stri = ''
        stri = a.split('/')[0]+'/'+a.split('/')[1]+'/'+a.split('/')[2]+'/'+a.split('/')[3]+'/'+a.split('/')[4]+'/'+dest[source.index(b)]+'/'+a.split('/')[6]
        lista.append(stri)
            
    df['_label']=list
    return(df)