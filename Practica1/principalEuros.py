#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:43:08 2019

@author: jose
"""
import financiacion as fc
def datos(mensaje,rangoInf,rangoSup = None):
    compro = False
    while compro == False:
        
        try:
            cantidad = float(input(mensaje))
            if rangoSup == None:
                if cantidad > rangoInf and fc.redondear(cantidad,2) == cantidad:
                    compro = True
                else:
                    compro = False
            else:
                if cantidad <= rangoSup and cantidad > rangoInf and fc.redondear(cantidad,2) == cantidad:
                    
                    compro = True
                else:
                    compro = False
                        
        except:
            print("error")
            compro = False
    return cantidad
#compro(cantidad,cantidad > 0 and fc.redondear(cantidad,2) == cantidad,)    
mensaje = "Introduzca una cantidad de euros mayor que 0 y maximo 2 deciamles: "
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
    except:
        compro = False


cantidadFinal = cantidad

for i in range(0,años):
    #cantidad_final += cantidad_final * interes
    cantidadFinal = fc.calcularCapitalFinal(cantidadFinal,interes)
 
    cantidadFinal = fc.redondear(cantidadFinal,2)
print("El total final es de: ", cantidadFinal)



