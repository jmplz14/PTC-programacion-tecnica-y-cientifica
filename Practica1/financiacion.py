#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:37:18 2019

@author: jose
"""
import math 
def redondear(numero,decimales):
    
    num_decimales = math.pow(10,decimales)
    numero=numero * num_decimales 
    numero=numero + 0.5
    numero=(int)(numero) # también se puede usar floor(numero)
    numero=numero / num_decimales

    return numero



def calcularCapitalFinal(capitalInicial, interes):
    total_intereses = capitalInicial * (interes/100)
    capitalFinal = capitalInicial + total_intereses
    return capitalFinal
    