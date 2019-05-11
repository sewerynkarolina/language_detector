import pdftotext
import re
from collections import Counter
from string import punctuation

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
        main_dict = Counter(dict(filter(lambda x: x[1] >= page_number/2, Counter(n_grams(file,i)).items())))
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
    


    