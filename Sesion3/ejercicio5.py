#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:14:15 2019

@author: jose
"""

def devolverMayus(letra):
    return  chr( ord(letra) - 32) 


def esVocal(letra):
    encontrada = False
    vocales = "aeiou"
    i = 0
    while i < 5 and not encontrada:
        mayuscula = devolverMayus(vocales[i])
        if vocales[i] == letra or mayuscula == letra:
            encontrada = True
        i += 1
    
    return encontrada

def numVocales(palabra):
    tamaño = len(palabra)
    numVocales = 0
    
    for i in range(tamaño):
        if esVocal(palabra[i]) == True:
            numVocales += 1
    return numVocales

def numVocalesPy(cadena):
    vocales = "aeiou"
    cadenaMinus = cadena.lower()
    numVocales = 0
    for i in vocales:
        numVocales += cadenaMinus.count(i)
        
    return numVocales
cadena = input("Introduce la cadena: ")
print("Ejercicio 5")
print("La cadena ({}) tiene {} vocales.".format(cadena,numVocales(cadena)))
print("La cadena ({}) tiene {} vocales.".format(cadena,numVocalesPy(cadena)))