path = '/home/marcin/Dane/'
import pandas as pd
import numpy as np

df = pd.read_pickle(path + "text.pkl").fillna('')[["label", "text"]].reset_index(drop=True)

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
from PyPDF2 import PdfFileReader
import PyPDF2


import pdftotext
def get_number_of_pages(file_paths):
    """
    Przyjmuje listę ścieżek pdfów, zwraca listę odpowiadających stron
    """
    num_of_page = [0]*len(file_paths)
    it = 0
    for text in file_paths:
        with open(text, "rb") as f:
            pdf = pdftotext.PDF(f)
            for page in pdf:
                num_of_page[it] += 1
            it+=1 
    return num_of_page


# Zmieniłem funkcję Kasi, dziala znacznie szybciej
def get_number_of_pages1(file_paths):
    """
    Przyjmuje listę ścieżek pdfów, zwraca listę odpowiadających stron
    """
    num_of_pages = []
    for i in range(len(file_paths)):
        try:
            pdf = PdfFileReader(open(files[i],'rb'))
            if pdf.isEncrypted:
                pdf.decrypt('')
            num_of_pages.append(pdf.getNumPages())
        except:
            print(i)
            num_of_pages.append(0)
    return num_of_pages


# Znaczniki konca strony z zaczytanych tekstow
def get_number_of_pages2(df):
    """
    Przyjmuje listę ścieżek pdfów, zwraca listę odpowiadających stron
    """
    num_of_pages = []
    
    for i in range(len(files)):
        num_of_pages.append(df["text"][i].count("\x0c"))
    return num_of_pages


# Liczenie stron wywala sie dla niektorych plikow :(

df = pd.read_pickle(path + "text_clean.pkl")
#df=df.head(1000)
files = df["label"]
text_cc = df["text_cc"]


#pages = get_number_of_pages(files)
#pages2 = get_number_of_pages2(df)
#df["no_pages"] = pages



text_c = ['']*df.shape[0]
for i in range(df.shape[0]):
    text_c[i] = prep_data.normalization(df['text'][i])
    text_c[i] = prep_data.normalize(text_c[i]) 
df["text_c"] = text_c


#df = pd.read_pickle(path + "text_clean.pkl")

files = df["label"]
text_c = df["text_c"]
text_cc = ['']*df.shape[0]
for i in range(df.shape[0]):
    text_cc[i] = prep_data.remove_intr_refe(text_c[i]) 
    text_cc[i] = prep_data.remove_footer(text_cc[i], 4)
    text_cc[i] = text_cc[i].replace("startstrona", "").replace("  ", " ").replace("  ", " ")
    if(i%500 == 0):
        print(i)
df["text_cc"] = text_cc



df.to_pickle(path + "text_clean.pkl")



#df["text"][6525]
#files[6525]
#pages = get_number_of_pages(files[6524:6526])
#
#
#i = 6525
#pdf = PdfFileReader(open(files[i],'rb'))
#if pdf.isEncrypted:
#    pdf.decrypt('')
#asd = pdf.getNumPages()
#asd



ii = range(100)
ii = range(df.shape[0]-100, df.shape[0])
ii = range(df.shape[0]-2000, df.shape[0]-2000+100)


for i in ii:
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(text_cc[i][0:2000])

for i in ii:
    print("\n" + "############ " + str(i) + ". - " + files[i] + "############\n")
    print(df["text"][i][0:1500])


i = 85
i = 98
i = 860

print(df["text"][i][0:100000].replace("\x0c", "\n\n"))
print(text_c[i][0:1000000].replace("startstrona", "\n\n"))
text_cc[i][0:1000000]
df["text"][i][0:100000]
files[i]


k = 0
for i in range(df.shape[0]):
    l = len(df["text"][i])
    l_c = len(df["text_c"][i])
    l_cc = len(df["text_cc"][i])
    if((l_cc == 0) & (l > 0)):
        print(i)
        k = k+1

k

i = 652
t=df["text"][i]
tt=prep_data.normalization(t)
tt
tt = prep_data.normalize(tt)
tt
prep_data.remove_footer0(tt, 4)
tasd = prep_data.remove_intr_refe(tt)
tasd

asd = df.iloc[i,:]
asd


dff=df.iloc[0:100,:]
