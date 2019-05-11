#import pdftotext
import re
from collections import Counter
from string import punctuation
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
#import pdftotext
import re
from nltk.stem import WordNetLemmatizer
import nltk
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
    
def read_files(file_paths):
    text_list = []
    num_of_page = [0]*len(file_paths)
    it = 0
    for text in file_paths:
        with open(text, "rb") as f:
            pdf = pdftotext.PDF(f)
            el_of_list = ''
            #Ponieważ page in pdf  - to jest strona z artykułu to łącze stringi, pewnie to można lepiej
  
            for page in pdf:
                el_of_list = el_of_list+" startstrona "+ page
                num_of_page[it] += 1
            it+=1
                
            text_list.append(el_of_list)  
            
    return (text_list, num_of_page)

def normalize(file):
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

def remove_intr_refe(file):
    head, sep, result = file.partition("ntroductio")
    result, sep, tail = result.rpartition("eferences")
    return(result)
    
def remove_footer(file,page_number, n_gram=25):

    
    for i in list(range(n_gram, 2,-1)):
        main_dict = Counter(dict(filter(lambda x: x[1] >= page_number/2 and "startstrona" in x[0], Counter(n_grams(file,i)).items())))
        if (main_dict!=Counter() ):
            break
    
    #Usuwam nagłówki
    for i in list(main_dict.keys()):
        if(i in file):
            file = file.replace(i,"")
            
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
    
def vectorizer_n_files(df, list_of_files_indexes, column_name='0'):
    """
    Funkcja która przekształca kolumnę dataframu z tekstem na macierz zliczeń
    zwracamy macierz i listę krajów
    """
    vec = CountVectorizer()
    X = vec.fit_transform(df.iloc[list_of_files_indexes][column_name])
    new_df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    
    return(new_df,df.iloc[list_of_files_indexes]['countries'].values ) 