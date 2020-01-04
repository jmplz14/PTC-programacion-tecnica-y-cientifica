#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 15:44:13 2020

@author: jose
"""
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from warnings import simplefilter
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing as pp



simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

scaler = MinMaxScaler()


cabecera = ["perimetro","profundiad","anchura","clase"]
datos = pd.read_csv("piernasDataset.csv", names=cabecera) 
datos[cabecera] = scaler.fit_transform(datos[cabecera])

X = datos.drop('clase', axis=1)  
"""print(X)
poly = PolynomialFeatures(degree=3, interaction_only=True)
poly = pp.PolynomialFeatures(2)
output_nparray = poly.fit_transform(X)
target_feature_names = ['x'.join(['{}^{}'.format(pair[0],pair[1]) for pair in tuple if pair[1]!=0]) for tuple in [zip(datos.columns,p) for p in poly.powers_]]
output_df = pd.DataFrame(output_nparray, columns = target_feature_names)
X=output_df
X = output_df"""

y = datos['clase'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=8)

svcLineal = SVC(kernel='linear')  
svcLineal.fit(X_train, y_train)

y_pred = svcLineal.predict(X_test)

acc_test=accuracy_score(y_test, y_pred)

print("Acc_test Lineal: (TP+TN)/(T+P)  %0.4f" % acc_test)

print("Matriz de confusión Filas: verdad Columnas: predicción")
'''
 Cij observaciones que son de clase i pero que se predicen a la clase j.
 La suma por filas son los ejemplos reales que hay de cada clase=soporte.
( TN	FP 
  FN	TP )
'''

print(confusion_matrix(y_test, y_pred))

'''
La precisión mide la capacidad del clasificador en no etiquetar como positivo un ejemplo que es negativo.
El recall mide la capacidad del clasificador para encontrar todos los ejemplos positivos.
'''

print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
print("f1-score es la media entre precisión y recall")
print(classification_report(y_test, y_pred))

svcLineal2 = SVC(kernel='linear')

scores = cross_val_score(svcLineal2, X, y, cv=5)

# exactitud media con intervalo de confianza del 95%
print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

print("----------------------------------------------------------------------------------------")

'''
KERNEL POLINOMICO
'''
grado=2

print("Clasificación con kernek polinomico de grado ", grado)

svcPol = SVC(kernel='poly', degree=grado)  
svcPol.fit(X_train, y_train)


# Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial

y_pred = svcPol.predict(X_test)

acc_test=accuracy_score(y_test, y_pred)

print("Acc_test Polinomico: (TP+TN)/(T+P)  %0.4f" % acc_test)

print("Matriz de confusión Filas: verdad Columnas: predicción")
'''
 Cij observaciones que son de clase i pero que se predicen a la clase j.
 La suma por filas son los ejemplos reales que hay de cada clase=soporte.
( TN	FP 
  FN	TP )
'''

print(confusion_matrix(y_test, y_pred))

'''
La precisión mide la capacidad del clasificador en no etiquetar como positivo un ejemplo que es negativo.
El recall mide la capacidad del clasificador para encontrar todos los ejemplos positivos.
'''

print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
print("f1-score es la media entre precisión y recall")
print(classification_report(y_test, y_pred))

#Para asegurarnos de que el resultado no depende del conjunto de test elegido
#tenemos que realizar validación cruzada

svcPol2 = SVC(kernel='poly', degree=grado)

scores = cross_val_score(svcPol2, X, y, cv=5)

# exactitud media con intervalo de confianza del 95%
print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))


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

svcRBF = SVC(kernel='rbf', gamma='auto') 
svcRBF.fit(X_train, y_train)


# Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial

y_pred = svcRBF.predict(X_test)

acc_test=accuracy_score(y_test, y_pred)

print("Acc_test RBF: (TP+TN)/(T+P)  %0.4f" % acc_test)

print("Matriz de confusión Filas: verdad Columnas: predicción")
'''
 Cij observaciones que son de clase i pero que se predicen a la clase j.
 La suma por filas son los ejemplos reales que hay de cada clase=soporte.
( TN	FP 
  FN	TP )
'''

print(confusion_matrix(y_test, y_pred))

'''
La precisión mide la capacidad del clasificador en no etiquetar como positivo un ejemplo que es negativo.
El recall mide la capacidad del clasificador para encontrar todos los ejemplos positivos.
'''

print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
print("f1-score es la media entre precisión y recall")
print(classification_report(y_test, y_pred))

#Para asegurarnos de que el resultado no depende del conjunto de test elegido
#tenemos que realizar validación cruzada

svcRBF2 = SVC(kernel='rbf', gamma='auto')

scores = cross_val_score(svcRBF2, X, y, cv=5)

# exactitud media con intervalo de confianza del 95%
print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))