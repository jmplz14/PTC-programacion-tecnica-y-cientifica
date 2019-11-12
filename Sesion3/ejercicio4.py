#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:19:52 2019

@author: jose
"""

cadena = input("Introduce una frase: ")
subcadena = input("Introduce la subcadena a buscar: ")

pos_inicio = -1
print("Metodo manual")
print("---------------------------------------")  
encontrada = False
tam_cadena = len(cadena)
tam_subcadena = len(subcadena)
i=0
while i < tam_cadena and i+tam_subcadena <= tam_cadena and  encontrada == False:
    j = 0
    distinta = False
    
    while j < tam_subcadena and distinta == False:
        if cadena[j+i] != subcadena[j]:
            distinta = True

        j += 1
    if distinta == False:
        encontrada = True
        pos_inicio = i
    else:
        i += 1

    
print("La subcadena empieza en {}".format(pos_inicio))
print("\n")


print("Metodo de string")
print("---------------------------------------")
pos_inicio = cadena.find(subcadena)
        
print("La subcadena empieza en {}".format(pos_inicio))