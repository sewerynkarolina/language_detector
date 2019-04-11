import numpy  as np
import nltk
import pandas as pd
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
#Ramka taka jak w wyniku create_matrix_from_file

def part_of_speech_tagger(path, list_of_st):

    df = pd.read_csv(path)
    #Ustawiam jako indeksy nazwy pliików
    df.index = df['Unnamed: 0']
    #Usuwam kolumnę z nazwami plików
    df.drop('Unnamed: 0', axis=1, inplace=True)
    #Liczba wierszy - ważne, bo będę dodawać jeden wiersz
    n = df.shape[0]
    
    #array z nazwami kolumn, usuwam ostatnią bo tam jest nazwa państwa
    words=df.columns.values
    words = words[:len(words)-1]
    
    #Tworze tuple z częściami mowy danego słowa
    tokenized_sents = [nltk.word_tokenize(i) for i in words]
    tuple_with_part = [nltk.pos_tag(i) for i in tokenized_sents]
    
    #Wyciągam samą część mowy
    parts = [tuple_with_part[i][0][1] for i in range(len(tuple_with_part))]
    
    #Wstawiam na koniec listy 'language' bo ostatnia kolumna to Państwa
    parts.append('language')
    
    #Wstawiam do naszego data frame'u części mowy i sprawdzam czy jest to część mowy z listy
    df.loc[len(df)] = parts
    mask = df.iloc[n].isin(list_of_st)
    
    #Jeżeli jest to ta kolumna będzie należeć do nowej macierzy
    col_keep = df.loc[:, mask]
    
    #Zapisuje i zwracam
    col_keep.iloc[:col_keep.shape[0]-1].to_csv('probna2.csv')
    return(col_keep.iloc[:col_keep.shape[0]-1])