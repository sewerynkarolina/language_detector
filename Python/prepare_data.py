#import pdftotext
import re
from collections import Counter
from string import punctuation
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
#import pdftotext
#import pdftotext

from nltk.stem import WordNetLemmatizer
import nltk
import unicodedata
nltk.download('wordnet')
import numpy as np
from nltk.corpus import words
nltk.download('words')

def n_grams(text, n=2):
    '''
    wymagania: modul re
    text - artykul, na podstawie ktorego chcemy uzyskac liste n gramow
    zalozenie - 1.text zostal wczesniej poddany zabiegom lematyzacji i czyszczenia
                2.type(text)==str
    n>2, type(n)==int
    '''
    if type(text) != str:
        raise NameError("Zly typ argumentu text, text musi byc typu str")
    if type(n) != int or n<2:
        raise NameError("n musi byc liczba calkowita, n>2")
    
    
    text = text.lower()
    tokens = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).split() #slowa z text zapisane do listy
    
    n_grams=list() #miejsce na n gramy
    
    for i in range(len(tokens)-n+1):
        s = tokens[i] 
        for j in range(1,n):
            s = s + " " + tokens[i+j]
        n_grams.append(s)
    
    return n_grams
    
# def read_files(file_paths):
#     text_list = []
#     num_of_page = [0]*len(file_paths)
#     it = 0
#     for text in file_paths:
#         with open(text, "rb") as f:
#             pdf = pdftotext.PDF(f)
#             el_of_list = ''
#             #Ponieważ page in pdf  - to jest strona z artykułu to łącze stringi, pewnie to można lepiej
  
#             for page in pdf:
#                 el_of_list = el_of_list+" startstrona "+ page
#                 num_of_page[it] += 1
#             it+=1
                
#             text_list.append(el_of_list)  
            
#     return (text_list, num_of_page)



def normalize(file):
    
    
    ################## Dodałem sporo rzeczy - MS ###################
    #\x0c to znak specjalny końca strony
    file = file.replace("\x0c", " startstrona ")
    
    if(len(file)>0):
        if(file.count("\n")/len(file)>0.3):
            file = file.replace("\n\n", "#").replace("-\n", "") .replace("\n", "").replace("#", " ")
#            print(str(i) + "##########")
        else:
            file = file.replace("-\n", "").replace("\n\n", "\n").replace("\n", " ")
    else:
        file = ""
    
    file = file.replace("-", " ").replace("/", " ")
    file = file.replace(" n t r o d u c t i o ", "ntroductio").\
            replace(" e f e r e n c e s ", "eferences").\
            replace("a b s t r a c t", "abstract").\
            replace("b i b l i o g r a p h y", "bibliography")
            
    ##################################################################
    
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

def remove_intr_refe0(file):
    head, sep, result = file.partition("ntroductio")
    result, sep, tail = result.rpartition("eferences")
    return(result)
    

def remove_intr_refe(file):
    result = file

    l = len(result)
    if(l==0):
        return(result)
        
    k1 = result.find("abstract")
    k2 = result.find("troductio")
    
    if((k1 < k2) & (k1!=-1)):
        head, sep, result1 = result.partition("abstract")
        l1 = len(result1)
        if(l1/l>0.6):
            result = result1
            
    elif((k2 < k1) & (k1!=-1)):
        head, sep, result1 = result.partition("ntroductio")
        l1 = len(result1)
        if(l1/l>0.6):
            result = result1
            

    k1 = result.find("bibliography")
    k2 = result.find("eferences")
    
    if(k1 > k2):
        result1, sep, tail = result.rpartition("bibliography")
        l1 = len(result1)
        if(l1/l>0.6):
            result = result1
   
           
    elif(k2 > k1):
        result1, sep, tail = result.rpartition("eferences")
        l1 = len(result1)
        if(l1/l>0.6):
            result = result1
           
        
    result = re.sub("^n ", "", result)
    result = re.sub(" r$", "", result)
    return(result)
    
# stara wersja
def remove_footer0(file,page_number, n_gram=25):
    for i in list(range(n_gram, 2,-1)):
        main_dict = Counter(dict(filter(lambda x: x[1] >= page_number/2 and "startstrona" in x[0], Counter(n_grams(file,i)).items())))
        if (main_dict!=Counter() ):
            break
    
    #Usuwam nagłówki
    for i in list(main_dict.keys()):
        print(i)
        if(i in file and 'startstrona' in file):
            file = file.replace(i,"")
            
    return(file)

# Wersja nowa.
def remove_footer(file,page_number, n_gram=25):
    for i in list(range(n_gram, 2,-1)):
        main_dict = Counter(dict(filter(lambda x: x[1] >= page_number/2 and "startstrona" in x[0], Counter(n_grams(file,i)).items())))
        if (main_dict==Counter()):
            continue
    # Jeżeli znalazł jedną, to nie znaczy, że kończymy zabawę.
    # Stopka i nagłowek mogą być różnej długości. Wcześniej usunęłoby 
    # tylko to dłuższe.
    
    #Usuwam nagłówki
        for r in list(main_dict.keys()):
            if(r in file and 'startstrona' in file):
                file = file.replace(r," startstrona ").replace("  ", " ")
            
    return(file)


def remove_short_words(text, max_length=3):
    """
    usuwa z tekstu slowa o dlugosci mniejszej lub rownej od max_length
    
    argumenty:
    text - wejsciowy test
    max_length - maksymalna dlugosc slow do usuniecia
    
    zwraca:
    tekst z usunietymi krotkimi slowami
    """
    short_word = re.compile(r'\W*\b\w{1,' + str(max_length) + r'}\b')
    return short_word.sub('', text)
    
    
    
def merge_df(df, df2):
    """
    Łączenie dwóch csv-ek i stworzenie kolumn z autorem i krajem
    """
    df2 =df2.rename(columns={'0':'country'})
    df['country']=df2['country']
    df=df.dropna()
    df=df.reset_index()[['0','country']] #Po usunieciu nanów usunęłam indeksy, więc od nowa
    country_list = []*df.size
    name_list = []*df.size
    for i in list(range(df.shape[0])):
        a = df['country'][i]
        country_list.append(a.split('/')[len(a.split('/'))-2])
        name_list.append(a.split('/')[len(a.split('/'))-1])
    df['countries']=country_list
    df['authors']=name_list
    return(df)

def make_lemmatization(df,column_name ='0'):
    wordnet_lemmatizer = WordNetLemmatizer()
    for i in list(range(df.shape[0])):
        string  = ''
        sentence_words = nltk.word_tokenize(df[column_name][i])
        for word in sentence_words:
            string = string + wordnet_lemmatizer.lemmatize(word, pos="v") + ' '
        df[column_name][i]=string
    return(df)

def make_lemmatization_for_one_file(tekst):
    wordnet_lemmatizer = WordNetLemmatizer()
    string  = ''
    sentence_words = nltk.word_tokenize(tekst)
    for word in sentence_words:
        string = string + wordnet_lemmatizer.lemmatize(word, pos="v") + ' '
    return(string)

def remove_short_words_which_not_exists(text, max_length=3):
    """
    Wewnętrzna funkcja pomocnicza do remove_short_words_from_df
    """
    words_to_remove = [word for word in np.unique(text.split()) if len(word) <= max_length and word not in words.words()]
    for i in words_to_remove:
        text =text.replace(i, "")
    return(text)

def remove_short_words_from_df(df, column_name, max_length=3):
    """
    Usuwa z tekstu (df) krótkie słowa, które nie istnieją
    """
    for i in list(range(df.shape[0])):
        df[column_name][i]= remove_short_words_which_not_exists(df[column_name][i], max_length)
    return (df)

def normalization(text):
    """
    Normalizacja NFKD czyli np. wyłapywanie znaków ktorych nie ma, np. ﬁnd
    """
    return (unicodedata.normalize('NFKD', text).encode('utf-8', 'ignore').decode("utf-8"))

def delete_nan(df, column_name='text'):
    """
    Zwraca dataframe z usunietymi rzędami w ktorych były nany w kolumnie column_name
    """
    df = df[pd.notnull(df['text'])]
    return(df.reset_index().drop('index', axis=1))

def vectorizer_n_files(df, list_of_files_indexes, min_gram, max_gram, column_name='0'):
    """
    Funkcja która przekształca kolumnę dataframu z tekstem na macierz zliczeń
    zwracamy macierz i listę krajów
    """
    vec = CountVectorizer(ngram_range=(min_gram,max_gram))
    X = vec.fit_transform(df.iloc[list_of_files_indexes][column_name])
    new_df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    
    return(new_df,df.iloc[list_of_files_indexes]['countries'].values ) 

def vectorizer_for_one_file(text, min_gram, max_gram):
    """
    Funkcja która przekształca teskst a macierz zliczeń
    zwracamy macierz i listę krajów
    """
    vec = CountVectorizer(ngram_range=(min_gram,max_gram))
    X = vec.fit_transform([text])
    new_df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    
    return(new_df) 





#import 
# def get_number_of_pages(file_paths):
#     """
#     Przyjmuje listę ścieżek pdfów, zwraca listę odpowiadających stron
#     """
#     num_of_page = [0]*len(file_paths)
#     it = 0
#     for text in file_paths:
#         with open(text, "rb") as f:
#             pdf = pdftotext.PDF(f)
#             for page in pdf:
#                 num_of_page[it] += 1
#             it+=1 
#     return num_of_page


from PyPDF2 import PdfFileReader

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
# wywala sie dla niektorych plikow :(


def prepare_to_model(file, columns, pages):
    """
    Funkcja, która przyjmuje plik jako string,
    czyści, tworzy 1gramy, ..., 5 gramy.
    columns - nazwy predyktorów w modelu,
    gdy brak predyktora w pliku, tworzy pustą komórkę z wartością zero
    """
 
    file = prep_data.normalization(file)
    file = prep_data.normalize(file) 
    file = prep_data.remove_intr_refe(file)
    file = prep_data.remove_footer(file, pages)
    file = file.replace("startstrona", "").replace("  ", " ").replace("  ", " ")
    file = prep_data.make_lemmatization_for_one_file(file)
    df = vectorizer_for_one_file(file, 1, 5)
    
    diff_to_del = list(set(df.columns)-set(columns))
    diff_to_add = list(set(columns)-set(df.columns))
    
    list_of_columns1 = set(df)-set(diff_to_del)
    list_of_columns2 = list_of_columns1.union(diff_to_add)
    
    df_ = pd.DataFrame([[0]*len(diff_to_add)], columns=diff_to_add)
    to_pred = pd.DataFrame(pd.concat([df_,df[list_of_columns1]], axis=0).fillna(0).sum()).transpose()
    
    return(to_pred)




# Znaczniki konca strony z zaczytanych tekstow
# Najszybszy sposób. Jeśli nie zaczytała się całość, 
# to daje nam tyle stron ile się zaczytało.
def get_number_of_pages2(df):
    """
    Przyjmuje listę ścieżek pdfów, zwraca listę odpowiadających stron
    """
    num_of_pages = []
    files = df["label"]
    for i in range(len(files)):
        num_of_pages.append(df["text"][i].count("\x0c"))
    return num_of_pages



###################
# Wczytanie danych
###################
    
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
# from six import BytesIO as StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
