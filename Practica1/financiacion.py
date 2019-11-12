#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:37:18 2019

@author: jose
"""
import math 
def redondear(numero,decimales):
    
    num_decimales = math.pow(10,decimales)
    if decimales > 0:
        numero=numero * num_decimales 
    numero=numero + 0.5
    numero=(int)(numero) # también se puede usar floor(numero)
    if decimales > 0:
        numero=numero / num_decimales

    return numero



def calcularCapitalFinal(capitalInicial, interes):
    total_intereses = capitalInicial * (interes/100)
    capitalFinal = capitalInicial + total_intereses
    return capitalFinal

if __name__ == "__main__":
    print("Estas ejecutando como main")
    print(redondear(10.556,2))
    print(calcularCapitalFinal(10.56,5.33))
    
if __name__ == "funciones":
    print("Estas ejecutando como modulo")