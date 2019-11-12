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



import financiacion as fc
def datos(mensaje,rangoInf,rangoSup = None):
    compro = False
    while compro == False:
        
        try:
            cantidad = float(input(mensaje))
            compro = True
            if rangoSup == None:
                if not (cantidad > rangoInf and fc.redondear(cantidad,2) == cantidad):
                    compro = False

            else:
                if not (cantidad <= rangoSup and cantidad > rangoInf and fc.redondear(cantidad,2) == cantidad):
                    compro = False

            
            if not compro:
                print("Metio un dato no valido")
                        
        except:
            print("Metio un dato no valido")
            compro = False
    return Decimal(cantidad)




#compro(cantidad,cantidad > 0 and fc.redondear(cantidad,2) == cantidad,)    
mensaje = "Introduzca una cantidad de euros mayor que 0 y maximo 2 decimales: "
cantidad = datos(mensaje,0)
#cantidad = fc.redondear(cantidad,2)
mensaje = "Introzduzca el porcentaje de interes en el intervalo [100,0) y maximo 2 deciamles: "
interes = datos(mensaje,0,100)


#interes = fc.redondear(interes,2)   
#interes = interes / 100

compro = False
while compro == False:
    try:
        años = int(input("Introduzca una cantidad de años mayor que 0: "))
        if años >= 1:
            compro = True
        else:
            compro = False
        if not compro:
                print("Metio un dato no valido")
    except:
        print("Metio un dato no valido")
        compro = False

cantidadFinal = cantidad
for i in range(0,años):
    #cantidad_final += cantidad_final * interes
    cantidadFinal = calcularCapitalFinal(cantidadFinal,interes)
    cantidadFinal = cantidadFinal.quantize(Decimal("1.00"))

print("El total final es de: ", cantidadFinal)