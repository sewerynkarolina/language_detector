# Podstawowe funkcje do "czyszczenia" macierzy słów.

# -------------------- podstawowe funkcje ---------------------------

import numpy as np

def match_only_letters(tab):
    """
    zostawia tylko słowa składające się z liter lub ' -
    """
    return tab.filter(regex="^[a-zA-Z\'\-]+$")

def remove_rare(tab,k=1):
    """
    dla k=1 usuwa słowa występujące tylko raz
    dla k=2           -||-          co najwyżej dwa razy
    ...
    """
    return tab.loc[:,tab.sum(axis=0)>k]

def remove_rare2(tab,k=1):
    """
    dla k=1 usuwa słowa występujące tylko w jednej pracy
    dla k=2           -||-          w co najwyżej dwóch pracach
    ...
    dla k=tab.shape[0]-1 zostają tylko słowa występujące w każdej z prac
    """
    return tab.loc[:,np.count_nonzero(tab,axis=0)>k]
    
# -------------------- funkcje wymagające słownika ---------------------------

import nltk
#nltk.download('stopwords')
#nltk.download('words')
from nltk.corpus import stopwords 
from nltk.corpus import words
stop_words = set(stopwords.words('english'))
word_list = words.words()

def remove_nondict_words(tab):
    """
    usuwa wszystkie słowa, których nie ma w słowniku
    uwaga: w słowniku nie ma na przykład liczby mnogiej, więc takie słowa też będą usuwane
        stąd przed wywołaniem tej funkcji trzeba będzie pewnie zrobić stemming/lematyzację
    """
    return tab[[col for col in tab.columns if col in word_list]]

def remove_stop_words(tab):
    """
    usuwa spójniki, przyimki itp.
    np.: 'under', 'in', 'yours', "she's", 'am', 'here' ...
    """
    return tab[[col for col in tab.columns if col not in stop_words]]
