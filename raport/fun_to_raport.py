from sklearn.metrics import confusion_matrix
import pandas as pd 
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from joblib import dump, load
import json


def df_merge(list_of_df, on):
    """
    Funkcja do łączenia dataframów z listy po kolumnie on
    """
    new_df = list_of_df[0]
    for i in list_of_df[1:]:
        new_df = new_df.merge(i, on = on)
    
    return new_df

def _label_to_country(df):
    """
    Jeżeli mamy w planach mergowanie to to funkcja po zmergowaniu
    Przyjmuje df z id: _label i zamieniam na _country
    """
    countries = []
    for i in df['_label']:
        countries.append(i.split('/')[5])
    df['_country']=countries
    df = df.drop("_label", axis=1)
    return df
    
def log_model(df,test_size,model_path):
    """
    Buduje model logistystyczny z penalty = l1, na podstawie df - dataframu
    Wpisujemy też wielkość próby testowej
    Funkcja zwraca dwa Seriesy z etykietami proby testowej i etykietami przewidywanymi przez model

    model_path - ścieżka gdzie chcemy zapisać model wraz z jego nazwą

    Zapisuje kolumny modelu do pliku json
    """
    X = df.drop("_country",axis=1)
    y = df['_country'].astype('category').cat.codes
    X = StandardScaler().fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=test_size, random_state=142)
    clf = LogisticRegression(C=1, penalty='l1', tol=0.001, solver='saga')
    
    clf.fit(X_train, y_train)

    dump(clf, model_path + '.joblib')

    with open(model_path + 'columns.json', "w") as f:
        json.dump(list(df.drop('_country', axis=1 ).columns), f)


    y_pred = clf.predict(X_test)
    
    return y_test, y_pred

def confu_matrix_for_categories(df,y_test,y_pred,label_column='_country'):
    """
    Funkcja która, zrobi macierz gdy naszy predyktory są intami (nie krajami!)
    Przyjmuje df - wczytaną macierz wraz z 
    label_column - kolumną labelek
    """
    mark = pd.DataFrame(list(df['_country']),list(df['_country'].astype('category').cat.codes)).drop_duplicates()
    mark = mark.to_dict()[0]
    
    y_test =pd.DataFrame(y_test)
    y_test = y_test.replace({0: mark})
    
    y_pred =pd.DataFrame(y_pred)
    y_pred = y_pred.replace({0: mark})
    
    countries = list(np.unique(df['_country'].values))
    matrix = pd.DataFrame(confusion_matrix(y_test, y_pred, labels=countries), columns=countries, index=countries)
    
    return matrix

def accuracy_and_f1(y_test, y_pred):
    """
    Wyświetla accuracy i f1 w modelu
    """
    acc = np.round(sum(y_test==y_pred)/len(y_test),2)
    f1 = np.round(f1_score(y_test, y_pred, average='macro'),2)
    print("Accuracy w modelu: " + str(acc) +"\nF1 score w modelu: "+str(f1))


def print_coef_for_predict(model, columns, predicted_value, how_many):
    """
    Funkcja, która printuje how_many współczynników które wpłynęły na przewidzianą wartość
    Przyjmuje model na którym przewidujemy, predicted_value i liczbę pierwszych predyktorów
    i columns - predyktory na których przewidywał
    """
    val = pd.DataFrame(pd.DataFrame(model.coef_).iloc[predicted_value]).values
    df = pd.DataFrame(val[0],columns).sort_values(by = 0, ascending = False).head(how_many).rename({0:'value'}, axis= 'columns')
    return df
    
