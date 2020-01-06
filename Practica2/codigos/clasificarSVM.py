#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 15:44:13 2020

@author: jose
"""
from joblib import dump
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split 
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, GridSearchCV


from warnings import simplefilter
import numpy as np
SEED = 60

def mostrarDatos(modelo, X_train, y_train, X_test, y_test,X,y,cv):
    
    modelo.fit(X_train, y_train)
    
    y_pred = modelo.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    print(confusion_matrix(y_test, y_pred))
    
    '''
     Cij observaciones que son de clase i pero que se predicen a la clase j.
     La suma por filas son los ejemplos reales que hay de cada clase=soporte.
    ( TN	FP 
      FN	TP )
    '''
    
    
    '''
    La precisión mide la capacidad del clasificador en no etiquetar como positivo un ejemplo que es negativo.
    El recall mide la capacidad del clasificador para encontrar todos los ejemplos positivos.
    '''
    
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))
    
    

    scores = cross_val_score(modelo, X, y, cv=cv, scoring='accuracy')
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
    """plot_confusion_matrix2(y_test, y_pred, [0,1], title="Matriz de confusion")
    plt.show()"""
    
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)





cabecera = ["perimetro","profundiad","anchura","clase"]
datos = pd.read_csv("piernasDataset.csv", names=cabecera) 
#datos[cabecera] = scaler.fit_transform(datos[cabecera])

X = datos.drop('clase', axis=1)  


y = datos['clase'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=SEED)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

print("Valores por defecto\n")
print("\n------------------------------------------------------------------------")
print("Kernel linear")
print("------------------------------------------------------------------------\n")
svcLineal = SVC(kernel='linear', random_state=SEED)  
mostrarDatos(svcLineal,X_train, y_train, X_test, y_test,X,y,cv)


print("\n------------------------------------------------------------------------")
print("Kernel Polinomico")
print("------------------------------------------------------------------------\n")
grado=2

print("Clasificación con kernek polinomico de grado ", grado)

svcPol = SVC(kernel='poly', degree=grado, random_state=SEED)  
mostrarDatos(svcPol,X_train, y_train, X_test, y_test,X,y,cv)
print()

print("\n------------------------------------------------------------------------")
print("Kernel rbf")
print("------------------------------------------------------------------------\n")

svcRBF = SVC(kernel='rbf',random_state=SEED)
mostrarDatos(svcRBF,X_train, y_train, X_test, y_test,X,y,cv)



print("\n------------------------------------------------------------------------")
print("Mejoras para linear")
print("------------------------------------------------------------------------\n")
mejoraLinear = SVC(kernel='linear', random_state=SEED)  

parametros = { "C": [0.1 ,1, 20 ,30, 10, 100, 1000]}
gridLinear = {
    "param_grid": parametros,
    "cv": cv,
    "n_jobs": -1,
    "scoring": "accuracy"
}



linear = GridSearchCV(mejoraLinear, **gridLinear)
mostrarDatos(linear,X_train, y_train, X_test, y_test,X,y,cv)

print("\n------------------------------------------------------------------------")
print("Mejoras para rbf")
print("------------------------------------------------------------------------\n")
mejoraRbf = SVC(kernel='rbf', random_state=SEED)  

parametros = { "C": [0.1 ,1, 20 ,30, 10, 100, 1000],
"gamma": [0.1,0.5,1,2,3,7,10]}
gridRbf = {
    "param_grid": parametros,
    "cv": cv,
    "n_jobs": -1,
    "scoring": "accuracy"
}



rbf = GridSearchCV(mejoraRbf, **gridRbf)
mostrarDatos(rbf,X_train, y_train, X_test, y_test,X,y,cv)


print("\n------------------------------------------------------------------------")
print("Elección")
print("------------------------------------------------------------------------\n")

print("\nEl mejor es rbf con los siguientes estimadores: \n")
print(rbf.best_estimator_)





dump(rbf, "modelo.joblib")