#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 08:43:30 2019

@author: jose
"""
cadena = input("Introduce una frase: ")

while True:
    letra = input("Introduce una unica letra a buscar: ")
    if (len(letra) == 1):
        break

print("Metodo manual")
print("---------------------------------------")  
numero_repeticiones = 0

for c in cadena:
    if (c == letra):
        numero_repeticiones += 1
        
print("Tenemos {} repeticiones".format(numero_repeticiones))
print("\n")


print("Metodo de string")
print("---------------------------------------")
numero_repeticiones = cadena.count(letra)
        
print("Tenemos {} repeticiones".format(numero_repeticiones))