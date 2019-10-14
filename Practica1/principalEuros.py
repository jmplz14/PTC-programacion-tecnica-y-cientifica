#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:43:08 2019

@author: jose
"""
import financiacion as fc

while(True):
    cantidad = float(input("Introduzca una cantidad de euros mayor que 0:"))
    if cantidad > 0:
        break
cantidad = fc.redondear(cantidad,2)
while(True):
    interes = float(input("Introzduzca el porcentaje de interes en el intervalo [100,0): "))
    if interes <= 100 and interes > 0:
        break
interes = fc.redondear(interes,2)   
#interes = interes / 100
while(True):
    años = int(input("Introduzca una cantidad de años mayor que 0: "))
    if años >= 1:
        break

cantidadFinal = cantidad

for i in range(0,años):
    #cantidad_final += cantidad_final * interes
    cantidadFinal = fc.calcularCapitalFinal(cantidadFinal,interes)
 
cantidadFinal = fc.redondear(cantidadFinal,2)
print("El total final es de: ", cantidadFinal)



