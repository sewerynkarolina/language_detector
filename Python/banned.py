import pandas as pd

lista = ['china', 'russian','poland','japan','vietnam','spain','turkey','spanish','italy',
        'france', 'russia','nguyen','chinese','beijing','uk','chinese','turkish','german',
        'tokyo','yang','polish']

def delete_banned_words(df):
    ind_col = []
    for i in df.columns:
        for j in lista:
            if j in i:
                ind_col.append(i)
    df = df.drop(ind_col, axis = 1)
    return(df)