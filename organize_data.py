import os
import numpy as np
import shutil
import glob

folder_list = ['Austria', 'Bagladesh', 'Bahrain', 'Bangladesh', 'China',
       'CzechRepublic', 'France', 'Georgia', 'Germany', 'Greece',
       'Hungary', 'Italy', 'Japan', 'Kuwait', 'Lithuania', 'Malaysia',
       'Oman', 'Poland', 'Portugal', 'Qatar', 'Russia', 'SaudiArabia',
       'Slovakia', 'Spain', 'Turkey', 'UK', 'USA',
       'UnitedArabEmirates', 'Vietnam']
    
source = ['Manjunath/Americans','niedzialek/American',
'felski/American','klosowski/Arab' ,
'Manjunath/Austrians', 'klosowski/Bangladeshi','felski/British',
'Manjunath/Czechs' ,'shah/Chinese',
'Manjunath/Chinese','niedzialek/English',
'ciurzycki/French' ,'dziwulski/French',
'Manjunath/French','niedzialek/German' ,
'Manjunath/Germans' ,'Manjunath/Greeks' ,
'Manjunath/Hungarians','konowrocki/Italian',
'Manjunath/Italians','ciurzycki/Japanese' ,
'Manjunath/Lithuanians' ,'slon/Malays','Manjunath/Poles' ,
'ciurzycki/Polish' ,'dziwulski/Portuguese',
'Manjunath/Portugiese','ciurzycki/Russian','felski/Russian',
'Manjunath/Russians','Manjunath/Slovakians',
'dziwulski/Spanish','Manjunath/Spanish',
'klosowski/Turkish','slon/Turks','klosowski/Vietnamese','suzonowicz/Chinese',
'dziwulski/Bangladeshi','zalewska/China','zalewska/Hungary','krynski/Vietnam','krynski/Greece',
'krynski/Poland','krynski/Malaysia',
'arushanyan/Georgia','arushanyan/UK',
'arushanyan/Japan','arushanyan/Bangladesh',
'koziol/USA','koziol/Japan',
'sznajder/Russia','sznajder/China',
'suzonowicz/Kuwait','suzonowicz/United Arab Emirates',
'suzonowicz/Oman','suzonowicz/Saudi Arabia',
'suzonowicz/Bahrain','suzonowicz/Qatar',
'shah/USA','shah/Russia', 'shah/Austria',
'shah/UK','shah/Malaysia','shah/France',
'sogbesan/USA','sogbesan/Poland','sogbesan/Lithuania',
'sogbesan/Germany','sogbesan/UK','dokurno/Turkey','dokurno/CzechRepublic',
'wisniewski/Kuwait','wisniewski/Vietnam','wisniewski/Spain']

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

findL = ['Americans',
'American','Arab' ,
'Austrians', 'Bangladeshi','British',
'Czechs' ,
'Chinese','English',
'French' ,'German' ,
'Germans' ,'Greeks' ,
'Hungarians','Italian',
'Italians','Japanese' ,
'Lithuanians' ,'Malays','Poles' ,
'Polish' ,'Portuguese',
'Portugiese','Russian',
'Russians','Slovakians',
'Spanish',
'Turkish','Turks','Vietnamese','Chinese',
'Bangladeshi']

replaceL = ['USA','USA','UnitedArabEmirates','Austria','Bangladesh',
'UK','CzechRepublic','China','UK','France','Germany','Germany',
'Greece','Hungary', 'Italy','Italy','Japan','Lithuania','Malaysia','Poland',
'Poland','Portugal','Portugal','Russia','Russia', 'Slovakia','Spain','Turkey',
'Turkey','Vietnam','China','Bangladesh']

def transfer_data(source_, dest_):

    for i in folder_list:
        if not os.path.exists(dest_+i):
            os.makedirs(dest_+i)

    for it in list(range(len(source))):
        for j in os.listdir(source_+source[it]):
            shutil.move(source_+source[it]+'/'+j, dest_+dest[it]+"/"+j)

def create_dictionary(dest_):
    """
    Zadziała tylko po usunięciu ' " ' w csvkach
    """
    with open(dest_+'dictionary.csv', 'w'):
        pass
    os.remove(source_+'Manjunath/Slovakians/dictionary.csv')

    list_of_dict = []
    for i in [x[0] for x in os.walk(source_)]:
        os.chdir(i)
        result = glob.glob('*.{}'.format('csv'))
        if result != []:
            list_of_dict.append(i+"/"+result[0])  

    new_dict=open(dest_+"dictionary.csv","a")

    for num in list_of_dict:
        for line in open(num):
            new_dict.write(line)    
    new_dict.close()

    df = pd.read_csv(dest_+"dictionary.csv", header=None)
    df[1] = df[1].replace(findL, replaceL)
    df.to_csv(dest_+"dictionary.csv",index=False)
