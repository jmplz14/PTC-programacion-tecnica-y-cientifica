#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:28:15 2019

@author: jose
"""

from decimal import Decimal


def calcularCapitalFinal(capitalInicial, interes):
    total_intereses = capitalInicial * (interes/100)
    capitalFinal = capitalInicial + total_intereses
    return capitalFinal



while(True):
    cantidad = Decimal(input("Introduzca una cantidad de euros mayor que 0:"))
    if cantidad > 0:
        break

while(True):
    interes = Decimal(input("Introzduzca el porcentaje de interes en el intervalo [100,0): "))
    if interes <= 100 and interes > 0:
        break
    
#interes = interes / 100
while(True):
    años = int(input("Introduzca una cantidad de años mayor que 0: "))
    if años >= 1:
        break
cantidadFinal = cantidad
for i in range(0,años):
    #cantidad_final += cantidad_final * interes
    cantidadFinal = calcularCapitalFinal(cantidadFinal,interes)
cantidadFinal = cantidadFinal.quantize(Decimal("1.00"))

print("El total final es de: ", cantidadFinal)