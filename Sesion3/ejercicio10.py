#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:37:25 2019

@author: jose
"""

def es_inversa(palabra1, palabra2):
    tam1 = len(palabra1)
    tam2 = len(palabra2)
    i = 0
    j = -1
    if (tam1 == tam2):
        iguales = True
        while i < tam1 and iguales:
            if (palabra1[i] != palabra2[ (i+1) * -1]):
                iguales = False
            i += 1
            j -= 1
        return iguales
    else:
        return False

def es_inversa_py(palabra1, palabra2):
    alReves = "".join(reversed(palabra1))
    if (palabra2 == alReves):
        return True
    else:
        return False

palabra1 = "hola"
palabra2 = "aloh"
if es_inversa(palabra1, palabra2):
    print("Es inversa")
else:
    print("No es inversa")


if es_inversa_py(palabra1, palabra2):
    print("Es inversa")
else:
    print("No es inversa")
