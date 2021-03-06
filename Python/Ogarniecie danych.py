path = '/home/marcin/Dane/'
import pandas as pd
import numpy as np

df = pd.read_pickle(path + "text.pkl")[["label", "text"]].reset_index(drop=True)

source = ['Americans','American', 'American','Arab', 'Austrians', \
          'Bangladeshi','British', 'Czechs' ,'Chinese', 'Chinese', \
          'English', 'French', 'French', 'French', 'German', \
          'Germans' ,'Greeks', 'Hungarians','Italian', 'Italians', \
          'Japanese', 'Lithuanians' ,'Malays','Poles', 'Polish', \
          'Portuguese', 'Portugiese','Russian','Russian',\
          'Russians','Slovakians', 'Spanish','Spanish', \
          'Turkish','Turks','Vietnamese','Chinese', 'Bangladeshi', \
          'China','Hungary','Vietnam','Greece', 'Poland','Malaysia', \
          'Georgia','UK', 'Japan','Bangladesh', 'USA','Japan', \
          'Russia','China', 'Kuwait','United Arab Emirates', \
          'Oman','Saudi Arabia', 'Bahrain','Qatar', 'USA','Russia', \
          'Austria', 'UK','Malaysia','France', 'USA','sogbesan/Poland', \
          'Lithuania', 'Germany','UK','Turkey','CzechRepublic', \
          'Kuwait','Vietnam','Spain']

dest = ['USA','USA','USA','UnitedArabEmirates','Austria','Bangladesh',\
        'UK','CzechRepublic','China','China','UK','France','France','France',\
        'Germany','Germany', 'Greece','Hungary', 'Italy','Italy','Japan', \
        'Lithuania','Malaysia','Poland', 'Poland','Portugal','Portugal', \
        'Russia','Russia','Russia', 'Slovakia','Spain','Spain','Turkey', \
        'Turkey','Vietnam','China','Bangladesh','China','Hungary','Vietnam',\
        'Greece','Poland','Malaysia', 'Georgia','UK','Japan','Bangladesh',\
        'USA','Japan', 'Russia','China', 'Kuwait','UnitedArabEmirates', \
        'Oman','SaudiArabia', 'Bahrain','Qatar','USA','Russia', \
        'Austria','UK','Malaysia', 'France','USA','Poland',\
        'Lithuania','Germany','UK','Turkey', \
        'CzechRepublic','Kuwait','Vietnam','Spain']


files = df["label"]

country_list= []
name_list = []

for f in files:
    k2 = f.rfind("/")
    k1 = f.rfind("/", 0, k2)
    k1, k2
    x = f[(k1+1):k2]
    y = f[(k2+1):len(f)]
    
    country_list.append(x)
    name_list.append(y)

df['country']=country_list
df['name']=name_list



for i in range(df.shape[0]):
    if df['country'][i] in source:
        where_in_source = source.index(df['country'][i])
        df['country'][i]= dest[where_in_source]


country_list = df['country']
np.sort(np.unique(country_list))

a = np.unique(np.array(country_list), return_counts=True)
pd.DataFrame({"Country": a[0], "count": a[1]}).sort_values("Country").reset_index(drop=True)
name_list=np.array(name_list)





import prepare_data as prep_data




#df = pd.read_pickle(path + "text_clean.pkl")
#df=df.head(1000)
#files = df["label"]
#text_cc = df["text_cc"]



text_c = ['']*df.shape[0]
for i in range(df.shape[0]):
    text_c[i] = prep_data.normalization(df['text'][i])
    text_c[i] = prep_data.normalize(text_c[i]) 
df["text_c"] = text_c
df.to_pickle(path + "text_clean.pkl")



#df = pd.read_pickle(path + "text_clean.pkl")
#files = df["label"]
#text_c = df["text_c"]

text_cc = ['']*df.shape[0]
for i in range(df.shape[0]):
    text_cc[i] = prep_data.remove_intr_refe(text_c[i]) 
    text_cc[i] = prep_data.remove_footer(text_cc[i], 4)
    text_cc[i] = text_cc[i].replace("startstrona", "").replace("  ", " ").replace("  ", " ")
    if(i%500 == 0):
        print(i)
df["text_cc"] = text_cc




#pages = get_number_of_pages(files)
pages = prep_data.get_number_of_pages2(df)
df["pages"]=pages

df.to_pickle(path + "text_clean.pkl")






df = pd.read_pickle(path + "text_clean.pkl")
files = df["label"]
text_c = df["text_c"]
text_cc = df["text_cc"]
pages=df["pages"]



ii = range(100)
ii = range(df.shape[0]-100, df.shape[0])
ii = range(df.shape[0]-2000, df.shape[0]-2000+100)


for i in ii:
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text_cc[i][0:1500])

for i in ii:
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(df["text"][i][0:1500])

df["text"][97]

files[98]
i = 85
i = 98
i = 8057

print(df["text"][i][0:100000].replace("\x0c", "\n\n"))
print(text_c[i][0:1000000].replace("startstrona", "\n\n"))
text_cc[i][0:1000000]
df["text_cc"][i][0:100000]
files[i]


k = 0
ll_cc = []
for i in range(df.shape[0]):
    l = len(df["text"][i])
    l_c = len(df["text_c"][i])
    l_cc = len(df["text_cc"][i])
    ll_cc.append(l_cc)
    if((l_cc == 0) & (l > 0)):
        print(i)
        k = k+1
k
# Nie ma artykłow, które byłyby niepuste przed oczyszceniem, 
# a po już tak


sum(np.array(pages)<9)
sum((pages >0) & (pages<6))
sum(pages == 0)
sum(np.array(ll_cc) == 0)


i0 = np.where((pages >0) & (pages<9))[0][1000]
i0
f=files[i0]
f
tasd = prep_data.convert_pdf_to_txt(f)

i = i0


t=df["text"][i]
t[0:100]
tasd[0:100]
t[(len(t)-200):len(t)]
tasd[(len(tasd)-200):len(tasd)]


tt=prep_data.normalization(t)
tt
tt = prep_data.normalize(tt)
tt
prep_data.remove_footer0(tt, 4)
tasd = prep_data.remove_intr_refe(tt)
tasd
files[62]
asd = df.iloc[i,:]
asd




t0 = df.iloc[i0,:]
