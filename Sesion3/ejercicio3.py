#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 08:59:06 2019

@author: jose
"""
cadena = input("Introduce una frase: ")
cadena_contraria = ""


print("Metodo manual")
print("---------------------------------------")  
numero_repeticiones = 0
distancia_ascii = 32
for c in cadena:
    posicion = ord(c)
    if (posicion >= 65 and posicion <= 90):
        cadena_contraria += chr(posicion + distancia_ascii)
    elif (posicion >= 97 and posicion <= 122):
        cadena_contraria += chr(posicion - distancia_ascii)
    else:
        cadena_contraria += c
        
print("La cadena obtenida es {}".format(cadena_contraria))
print("\n")


print("Metodo de string")
print("---------------------------------------")
cadena_contraria = cadena.swapcase()
        
print("La cadena obtenida es {}".format(cadena_contraria))
