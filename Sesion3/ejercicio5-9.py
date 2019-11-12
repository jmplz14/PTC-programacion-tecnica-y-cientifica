#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:19:13 2019

@author: jose
"""

def devolverMayus(letra):
    return  chr( ord(letra) - 32) 
def esVocal(letra):
    encontrada = False
    vocales = ("a", "e", "i", "o", "u")
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

def numVocalesPy()
def vocalesContenidas(palabra):
    vocales = ["a", "e", "i", "o", "u"]
    vocalesEncontradas = []
    i = 0
    tamaño = len(palabra)
    todasVocales = False
    
    while i < tamaño and not todasVocales:
        j = 0
        encontrada = False
        
        while j < len(vocales) and not encontrada:
            mayuscula = devolverMayus(vocales[j])
            if vocales[j] == palabra[i] or mayuscula == palabra[i]:
                encontrada = True
                vocalesEncontradas.append(vocales[j])
                del vocales[j]
                
            j += 1
            
        if len(vocales) == 0:
            todasVocales = True
        i += 1
    return vocalesEncontradas



def vocalesContenidasPy(cadena):
    vocales = ("a", "e", "i", "o", "u")
    vocalesEncontradas = []
    cadenaMinus = cadena.lower()
    for i in vocales:
        if cadenaMinus.find(i) != -1:
            vocalesEncontradas.append(i)
    return vocalesEncontradas

def cadenaMayus(cadena):
    tamaño = len(cadena)
    cadenaMayus = ""
    for i in range(tamaño):
        enteroLetra = ord(cadena[i])
        if enteroLetra >= 97 and enteroLetra <= 122:
            cadenaMayus += chr(enteroLetra - 32)
        else:
            cadenaMayus += cadena[i]
    return cadenaMayus

def eliminarVocales(cadena):
    tamaño = len(cadena)
    cadenaSinVocales = ""
    for i in range(tamaño):
        if not esVocal(cadena[i]):
            cadenaSinVocales += cadena[i]

    return cadenaSinVocales

def terminaEmiezaVocal(cadena):
    if esVocal(cadena[0]) and esVocal(cadena[-1]):
        return True
    else:
        return False

cadena = "ahola"
print("Ejercicio 5")
print("La cadena ({}) tiene {} vocales.".format(cadena,numVocales(cadena)))

print("Ejercicio 6")
print("La cadena ({}) contiene las vocales {}.".format(cadena,vocalesContenidas(cadena)))
print("La cadena ({}) contiene las vocales {}.".format(cadena,vocalesContenidasPy(cadena)))

print("Ejercicio 7")
print("La cadena ({}) en mayusculas es: {}".format(cadena,cadenaMayus(cadena)))
print("La cadena ({}) en mayusculas es: {}".format(cadena,cadena.upper()))

print("Ejericio 8")

if terminaEmiezaVocal(cadena):
    print("La cadena {} termina y empieza por una vocal".format(cadena))
else:
    print("La cadena {} no termina y no empieza por una vocal".format(cadena))

print("Ejercicio 9")

print("La cadena ({}) sin vocales es: {}".format(cadena,eliminarVocales(cadena)))











