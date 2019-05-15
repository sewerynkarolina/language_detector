path = '/home/marcin/Dane/'

import pandas as pd
import re
from string import punctuation
import numpy as np

def normalize2(file):
    
    #\x0c to znak specjalny końca strony
    file = file.replace("\x0c", " startstrona ")
    file = " startstrona " + file
    
    file = re.sub("[0-9]", "", file)

    #zmiana na małe litery
    file = file.lower()
    #Zmieniamy np. ó na o
    file = re.sub(r'[^\x20-\x7e]', '', file)
    #usuwanie cyfry
    file = re.sub(r'\d+', '', file)
    #usuwanie znaków specjalne
    file = ''.join(c for c in file if c not in punctuation)
    #Usuwamy  białe spacje
    file = re.sub(' +', ' ', file)
    return(file)
    
    
data0 = pd.read_csv(path + "text0.csv").fillna('')
data1 = pd.read_csv(path + "text1.csv").fillna('')
data2 = pd.read_csv(path + "text2.csv").fillna('')


data = data0
data = data.append(data1, ignore_index = True).drop(data0.columns[0], axis=1)
data = data.append(data2, ignore_index = True).drop(data0.columns[0], axis=1)

del data0
del data1
del data2


text = data["text"]
files = data["label"]


# Ujednolicenie oznaczeń państw

nationality = []
for f in files:
    k2 = f.rfind("/")
    k1 = f.rfind("/", 0, k2)
    k1, k2
    x = f[(k1+1):k2]
    
    xx = x.replace("Americans", "USA").replace("Austrians", "Austria").\
    replace("Bangladeshi", "Bangladesh").replace("Chinese", "China").\
    replace("Czechs", "CzechRepublic").replace("French", "France").\
    replace("Germans", "Germany").replace("Greeks", "Greece").\
    replace("Hungarians", "Hungary").replace("Italians", "Italy").\
    replace("Japanese", "Japan").replace("Lithuanians", "Lithuania").\
    replace("Poles", "Poland").replace("Polish", "Poland").\
    replace("Portuguese", "Portugal").replace("Russians", "Russia").\
    replace("Russian", "Russia").replace("Slovakians", "Slovakia").\
    replace("Spanish", "Spain").replace("Turks", "Turkey").\
    replace("Portugiese", "Portugal").\
    replace("Malays", "X").replace("Xia", "Malaysia").replace("X", "Malaysia")
    
    nationality.append(xx)

np.sort(np.unique(nationality))

a = np.unique(np.array(nationality), return_counts=True)
pd.DataFrame({"Country": a[0], "count": a[1]}).sort_values("Country").reset_index(drop=True)




import ftfy
text_clean = []
text_n = []

for i in range(len(text)):  
#for i in range(100):  
    t = text[i]
        
    # fix text usuwa ligatury (kilka liter połączonych w jeden znak, np. ff, fi)
    t = ftfy.fix_text(t)
    
    # Wypatrzone przeze mnie znaki specjalne, których nie udało się podmienić
    t = t.replace("\x80", "ff")
    t = t.replace("®", "fi")

    # Zdarzały się pdfy, ktore zaczytały się tak, że miedzy każdymi literami było \n
    # Jeżeli \n stanowi ponad 1/3 znaków, to usuwam
    if(len(t)>0):
        if(t.count("\n")/len(t)>0.3):
            t2 = t.replace("\n\n", "#").replace("-\n", "") .replace("\n", "").replace("#", " ")
#            print(str(i) + "##########")
        else:
            t2 = t.replace("-\n", "").replace("\n\n", "\n").replace("\n", " ")
    else:
        t2 = ""
    
    text_clean.append(t2)
    
    t3 = normalize2(t2)
    text_n.append(t3)
    
    if(i%100==0):
        print(i)



ii = range(len(text))
ii = range(100)

for i in ii:
    print("\x0c" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text[i][0:1000])

for i in ii:
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text_clean[i][0:1000])

for i in ii:
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text_n[i][0:1000])
    



k = 5470
print(text_n[k].replace("startstrona", "\n\n")[0:10000])
print(text_clean[k].replace("startstrona", "\n\n")[0:10000])
text[k][0:1500]
text_clean[k][0:150]
text_n[k][0:150]
files[k]


