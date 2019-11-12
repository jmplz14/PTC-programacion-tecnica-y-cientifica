#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 08:59:06 2019

@author: jose
"""
cadena = input("Introduce una frase: ")
cadena_eliminada = ""
while True:
    letra = input("Introduce una unica letra a buscar: ")
    if (len(letra) == 1):
        break

print("Metodo manual")
print("---------------------------------------")  
numero_repeticiones = 0

for c in cadena:
    if (c != letra):
        cadena_eliminada += c
        
print("La cadena obtenida es {}".format(cadena_eliminada))
print("\n")


print("Metodo de string")
print("---------------------------------------")
cadena_eliminada = cadena.replace(letra,"")
        
print("La cadena obtenida es {}".format(cadena_eliminada))
