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
    

def plot_confusion_matrix2(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    #classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]



    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='Valores validos',
           xlabel='Valores predecidos')
    plt.xlim(-0.5, 2-0.5)
    plt.ylim(2-0.5, -0.5)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax



simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)




cabecera = ["perimetro","profundiad","anchura","clase"]
datos = pd.read_csv("piernasDataset.csv", names=cabecera) 
#datos[cabecera] = scaler.fit_transform(datos[cabecera])

X = datos.drop('clase', axis=1)  


y = datos['clase'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=SEED)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)


svcLineal = SVC(kernel='linear', random_state=SEED)  
mostrarDatos(svcLineal,X_train, y_train, X_test, y_test,X,y,cv)



print("----------------------------------------------------------------------------------------")

'''
KERNEL POLINOMICO
'''
grado=2

print("Clasificación con kernek polinomico de grado ", grado)

svcPol = SVC(kernel='poly', degree=grado, random_state=SEED)  
mostrarDatos(svcPol,X_train, y_train, X_test, y_test,X,y,cv)


print("----------------------------------------------------------------------------------------")
'''
KERNEL RADIAL

Parámetros

C: por defecto vale 1.0. Penaliza el error de clasificación de los ejemplos,
   a mayor valor más se ajusta al conjunto de ejemplos.
gamma: por defecto auto = 1/ num_características
    inversa del tamaño del "radio" del kernel. Una valor grande genera muchos
    conjuntos de radios pequeños
'''
print("Clasificación con kernek de base radial con C=1 y gamma=auto")

svcRBF = SVC(kernel='rbf', random_state=SEED)
mostrarDatos(svcRBF,X_train, y_train, X_test, y_test,X,y,cv)


final = SVC(kernel='rbf', random_state=SEED)  
parametros = { "C": [10, 100, 1000,10000],
"gamma": [0.1, 0.07, 0.5]
}


grid = {
    "param_grid": parametros,
    "cv": cv,
    "n_jobs": -1,
    "scoring": "accuracy"
}
mejor_svm = GridSearchCV(final, **grid)
mejor_svm.fit(X_train, y_train)


print("\n-------------------- Mejor estimador --------------------")
print(mejor_svm.best_estimator_)

modelo_final = SVC(kernel="rbf", random_state=SEED, **mejor_svm.best_params_)
modelo_final.fit(X, y)

dump(modelo_final, "modelo.joblib")