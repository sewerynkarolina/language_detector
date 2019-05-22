path = '/home/marcin/Dane/'
import pandas as pd
import numpy as np
import prepare_data as prep_data


df = pd.read_pickle(path + "file1.pkl")


import nltk
import pandas as pd
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
#Ramka taka jak w wyniku create_matrix_from_file

col = df.columns
A = []

for i in range(len(col)):
    c = col[i]
    pp = nltk.pos_tag(nltk.word_tokenize(c))
    a = ""
    for k in range(len(pp)):
        a = a + "_" + pp[k][1]
    A.append(a)





pos = pd.DataFrame()
for p in np.unique(A):

    np.where(p == np.array(A))
    pos[p] = df[df.columns[np.where(p == np.array(A))]].sum(axis = 1)


pos








